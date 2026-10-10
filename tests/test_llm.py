import json

import httpx
import llm
import pytest

KEY_B = "key-openrouter-654321"
KEY_C = "key-openai-abcdef"
ENV = {
    "FRAMESMITH_LLM_PROVIDERS": "openrouter,ollama,openai",
    "FRAMESMITH_OPENROUTER_API_KEY": KEY_B,
    "FRAMESMITH_OPENROUTER_MODEL": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "FRAMESMITH_OPENAI_API_KEY": KEY_C,
    "FRAMESMITH_OPENAI_MODEL": "gpt-6-luna",
    "FRAMESMITH_OLLAMA_MODEL": "qwen3.5:4b-q4_K_M",
}


def client_for(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def openai_reply(text):
    return httpx.Response(200, json={"choices": [{"message": {"content": text}}]})


def needs_ok(data):
    if isinstance(data, dict) and data.get("ok") is True:
        return data, []
    return data, ["field 'ok' must be true"]


def run(handler, env=ENV):
    sleeps: list[float] = []
    result = llm.generate_json(
        "system", "user", needs_ok, env, client=client_for(handler), sleep=sleeps.append
    )
    return result, sleeps


def test_extract_json_handles_fences_and_prose():
    assert llm.extract_json('```json\n{"a": 1}\n```') == {"a": 1}
    assert llm.extract_json('Sure! Here it is: {"a": 1} Hope that helps.') == {"a": 1}
    with pytest.raises(ValueError):
        llm.extract_json("no json here")
    with pytest.raises(ValueError):
        llm.extract_json("{broken")


def test_falls_back_after_retryable_errors():
    calls = {"openrouter": 0, "ollama": 0, "openai": 0}

    def handler(request):
        if request.url.host == "openrouter.ai":
            calls["openrouter"] += 1
            return httpx.Response(503, text="overloaded")
        if request.url.path == "/api/chat":
            calls["ollama"] += 1
            return httpx.Response(200, json={"message": {"content": '{"ok": true}'}})
        calls["openai"] += 1
        return openai_reply('{"ok": true}')

    result, sleeps = run(handler)
    assert result.provider == "ollama"
    assert calls == {"openrouter": 3, "ollama": 1, "openai": 0}  # local fallback precedes paid API
    assert len(sleeps) == 2  # backoff between the 3 attempts, none after the last


def test_non_retryable_status_skips_straight_to_next_provider():
    calls = {"openrouter": 0}

    def handler(request):
        if request.url.host == "openrouter.ai":
            calls["openrouter"] += 1
            return httpx.Response(401, text="API key not valid")
        return openai_reply('{"ok": true}')

    result, sleeps = run(handler, {**ENV, "FRAMESMITH_LLM_PROVIDERS": "openrouter,openai"})
    assert result.provider == "openai" and calls["openrouter"] == 1 and sleeps == []


def test_invalid_output_is_fed_back_and_retried():
    bodies = []

    def handler(request):
        bodies.append(json.loads(request.content))
        text = "not json at all" if len(bodies) == 1 else '{"ok": true}'
        return openai_reply(text)

    result, _ = run(handler, {**ENV, "FRAMESMITH_LLM_PROVIDERS": "openrouter,openai"})
    assert result.provider == "openrouter" and result.attempts == 2
    second_prompt = bodies[1]["messages"][1]["content"]
    assert "rejected" in second_prompt and "not valid JSON" in second_prompt


def test_schema_style_rejection_is_fed_back():
    bodies = []

    def handler(request):
        bodies.append(json.loads(request.content))
        return openai_reply('{"ok": false}' if len(bodies) == 1 else '{"ok": true}')

    result, _ = run(handler)
    assert result.attempts == 2
    assert "field 'ok' must be true" in bodies[1]["messages"][1]["content"]


def test_openrouter_uses_bearer_header():
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("authorization")
        seen["body"] = json.loads(request.content)
        return openai_reply('{"ok": true}')

    env = {**ENV, "FRAMESMITH_LLM_PROVIDERS": "openrouter"}
    result, _ = run(handler, env)
    assert result.provider == "openrouter"
    assert seen["auth"] == f"Bearer {KEY_B}"
    assert "nvidia/nemotron-3-ultra-550b-a55b:free" == seen["body"]["model"]
    assert "response_format" not in seen["body"]


def test_openai_uses_chat_completions_json_mode_and_bearer_header():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("authorization")
        seen["body"] = json.loads(request.content)
        return openai_reply('{"ok": true}')

    env = {**ENV, "FRAMESMITH_LLM_PROVIDERS": "openai"}
    result, _ = run(handler, env)
    assert result.provider == "openai" and result.model == "gpt-6-luna"
    assert seen["url"] == "https://api.openai.com/v1/chat/completions"
    assert seen["auth"] == f"Bearer {KEY_C}"
    assert seen["body"]["model"] == "gpt-6-luna"
    assert seen["body"]["response_format"] == {"type": "json_object"}
    assert seen["body"]["reasoning_effort"] == "none"
    assert seen["body"]["temperature"] == 0.9


def test_ollama_uses_local_chat_api_without_api_key():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["auth"] = request.headers.get("authorization")
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"message": {"content": '{"ok": true}'}})

    env = {**ENV, "FRAMESMITH_LLM_PROVIDERS": "ollama"}
    result, _ = run(handler, env)
    assert result.provider == "ollama" and result.model == "qwen3.5:4b-q4_K_M"
    assert seen["url"] == "http://127.0.0.1:11434/api/chat"
    assert seen["auth"] is None
    assert seen["body"]["model"] == "qwen3.5:4b-q4_K_M"
    assert seen["body"]["stream"] is False
    assert seen["body"]["format"] == "json"
    assert seen["body"]["think"] is False


def test_total_failure_message_never_contains_keys():
    def handler(request):
        return httpx.Response(500, text=f"boom {KEY_B} {KEY_C}")

    with pytest.raises(llm.LLMError) as caught:
        run(handler)
    message = str(caught.value)
    assert "all providers failed" in message
    assert all(key not in message for key in (KEY_B, KEY_C))


def test_provider_without_model_or_key_is_skipped():
    env = {
        "FRAMESMITH_LLM_PROVIDERS": "gemini,opencode,openrouter,ollama,openai",
        "FRAMESMITH_GEMINI_API_KEY": "stale-gemini-key",
        "FRAMESMITH_GEMINI_MODEL": "stale-model",
        "FRAMESMITH_OLLAMA_MODEL": "qwen3.5:4b-q4_K_M",
        "FRAMESMITH_OPENROUTER_API_KEY": KEY_B,
        "FRAMESMITH_OPENROUTER_MODEL": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "FRAMESMITH_OPENAI_API_KEY": KEY_C,
        "FRAMESMITH_OPENAI_MODEL": "gpt-6-luna",
    }
    providers, skipped = llm.configured_providers(env)
    assert [provider.name for provider in providers] == ["openrouter", "ollama", "openai"]
    assert skipped == [
        "gemini: unknown provider",
        "opencode: unknown provider",
    ]


def test_default_provider_order_uses_verified_free_endpoint_first():
    env = {key: value for key, value in ENV.items() if key != "FRAMESMITH_LLM_PROVIDERS"}
    providers, skipped = llm.configured_providers(env)
    assert skipped == []
    assert [provider.name for provider in providers] == ["openrouter", "ollama", "openai"]


def test_no_usable_provider_raises_clear_error():
    with pytest.raises(llm.LLMError, match="no usable LLM provider"):
        llm.generate_json("s", "u", needs_ok, {}, client=client_for(lambda r: None))


def test_retry_count_comes_from_env():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(500)

    env = {**ENV, "FRAMESMITH_LLM_PROVIDERS": "openrouter", "FRAMESMITH_LLM_MAX_RETRIES": "2"}
    with pytest.raises(llm.LLMError):
        run(handler, env)
    assert calls["n"] == 2


def test_network_error_is_retried_then_falls_back():
    def handler(request):
        if request.url.host == "openrouter.ai":
            raise httpx.ConnectError("no route")
        return httpx.Response(200, json={"message": {"content": '{"ok": true}'}})

    result, sleeps = run(handler)
    assert result.provider == "ollama" and len(sleeps) == 2
