import json

import httpx
import llm
import pytest

KEY_A = "key-gemini-123456"
KEY_B = "key-groq-654321"
ENV = {
    "FRAMESMITH_LLM_PROVIDERS": "gemini,groq",
    "FRAMESMITH_GEMINI_API_KEY": KEY_A,
    "FRAMESMITH_GEMINI_MODEL": "gem-model",
    "FRAMESMITH_GROQ_API_KEY": KEY_B,
    "FRAMESMITH_GROQ_MODEL": "groq-model",
}


def client_for(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def gemini_reply(text):
    return httpx.Response(200, json={"candidates": [{"content": {"parts": [{"text": text}]}}]})


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


def test_gemini_key_goes_in_header_not_url():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["header"] = request.headers.get("x-goog-api-key")
        seen["body"] = json.loads(request.content)
        return gemini_reply('{"ok": true}')

    result, _ = run(handler)
    assert result.provider == "gemini" and result.model == "gem-model"
    assert seen["header"] == KEY_A and KEY_A not in seen["url"]
    assert "gem-model:generateContent" in seen["url"]
    assert seen["body"]["generationConfig"]["responseMimeType"] == "application/json"


def test_falls_back_after_retryable_errors():
    calls = {"gemini": 0, "groq": 0}

    def handler(request):
        if request.url.host.startswith("generativelanguage"):
            calls["gemini"] += 1
            return httpx.Response(503, text="overloaded")
        calls["groq"] += 1
        return openai_reply('{"ok": true}')

    result, sleeps = run(handler)
    assert result.provider == "groq"
    assert calls == {"gemini": 3, "groq": 1}  # 3 attempts, then fallback
    assert len(sleeps) == 2  # backoff between the 3 attempts, none after the last


def test_non_retryable_status_skips_straight_to_next_provider():
    calls = {"gemini": 0}

    def handler(request):
        if request.url.host.startswith("generativelanguage"):
            calls["gemini"] += 1
            return httpx.Response(401, text="API key not valid")
        return openai_reply('{"ok": true}')

    result, sleeps = run(handler)
    assert result.provider == "groq" and calls["gemini"] == 1 and sleeps == []


def test_invalid_output_is_fed_back_and_retried():
    bodies = []

    def handler(request):
        bodies.append(json.loads(request.content))
        text = "not json at all" if len(bodies) == 1 else '{"ok": true}'
        return gemini_reply(text)

    result, _ = run(handler)
    assert result.provider == "gemini" and result.attempts == 2
    second_prompt = bodies[1]["contents"][0]["parts"][0]["text"]
    assert "rejected" in second_prompt and "not valid JSON" in second_prompt


def test_schema_style_rejection_is_fed_back():
    bodies = []

    def handler(request):
        bodies.append(json.loads(request.content))
        return gemini_reply('{"ok": false}' if len(bodies) == 1 else '{"ok": true}')

    result, _ = run(handler)
    assert result.attempts == 2
    assert "field 'ok' must be true" in bodies[1]["contents"][0]["parts"][0]["text"]


def test_groq_uses_json_mode_and_bearer_header():
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("authorization")
        seen["body"] = json.loads(request.content)
        return openai_reply('{"ok": true}')

    env = {**ENV, "FRAMESMITH_LLM_PROVIDERS": "groq"}
    result, _ = run(handler, env)
    assert result.provider == "groq"
    assert seen["auth"] == f"Bearer {KEY_B}"
    assert seen["body"]["response_format"] == {"type": "json_object"}


def test_ollama_uses_native_chat_endpoint():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        seen["body"] = json.loads(request.content)
        return httpx.Response(200, json={"message": {"content": '{"ok": true}'}})

    env = {"FRAMESMITH_LLM_PROVIDERS": "ollama", "FRAMESMITH_OLLAMA_MODEL": "local-model"}
    result, _ = run(handler, env)
    assert result.provider == "ollama"
    assert seen["url"].endswith("/api/chat")
    assert seen["body"]["format"] == "json" and seen["body"]["stream"] is False


def test_total_failure_message_never_contains_keys():
    def handler(request):
        return httpx.Response(500, text=f"boom {KEY_A} {KEY_B}")

    with pytest.raises(llm.LLMError) as caught:
        run(handler)
    message = str(caught.value)
    assert "all providers failed" in message
    assert KEY_A not in message and KEY_B not in message


def test_provider_without_model_or_key_is_skipped():
    env = {
        "FRAMESMITH_LLM_PROVIDERS": "gemini,groq,openrouter",
        "FRAMESMITH_GEMINI_API_KEY": KEY_A,  # no model
        "FRAMESMITH_GROQ_MODEL": "groq-model",  # no key
        "FRAMESMITH_OPENROUTER_API_KEY": "k",
        "FRAMESMITH_OPENROUTER_MODEL": "free-model",
    }
    providers, skipped = llm.configured_providers(env)
    assert [p.name for p in providers] == ["openrouter"]
    assert len(skipped) == 2


def test_no_usable_provider_raises_clear_error():
    with pytest.raises(llm.LLMError, match="no usable LLM provider"):
        llm.generate_json("s", "u", needs_ok, {}, client=client_for(lambda r: None))


def test_retry_count_comes_from_env():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(500)

    env = {**ENV, "FRAMESMITH_LLM_PROVIDERS": "gemini", "FRAMESMITH_LLM_MAX_RETRIES": "2"}
    with pytest.raises(llm.LLMError):
        run(handler, env)
    assert calls["n"] == 2


def test_network_error_is_retried_then_falls_back():
    def handler(request):
        if request.url.host.startswith("generativelanguage"):
            raise httpx.ConnectError("no route")
        return openai_reply('{"ok": true}')

    result, sleeps = run(handler)
    assert result.provider == "groq" and len(sleeps) == 2
