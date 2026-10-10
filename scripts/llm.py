"""LLM calls with JSON validation, retries and provider fallback (blueprint R5, R11).

Providers are tried in FRAMESMITH_LLM_PROVIDERS order: openrouter, opencode, openai.
Model names are never hard-coded: set FRAMESMITH_<PROVIDER>_MODEL in .env.
API keys travel in request headers only and never appear in raised messages.
"""

from __future__ import annotations

import json
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import httpx

KNOWN_PROVIDERS = ("gemini", "openrouter", "opencode", "openai", "ollama")
DEFAULT_ORDER = "openrouter,opencode,openai"
NEEDS_KEY = {"gemini", "openrouter", "opencode", "openai"}
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENCODE_URL = "https://opencode.ai/zen/v1/chat/completions"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
OLLAMA_DEFAULT_URL = "http://127.0.0.1:11434"
RETRYABLE_STATUS = {408, 425, 429, 500, 502, 503, 504}

# check(data) -> (possibly normalized data, list of problems). Empty list means valid.
Check = Callable[[Any], tuple[Any, list[str]]]


class LLMError(RuntimeError):
    """No provider produced a valid answer, or a provider reply was malformed."""


class ProviderHTTPError(RuntimeError):
    def __init__(self, status: int, detail: str, retry_after: float | None = None) -> None:
        super().__init__(f"HTTP {status}")
        self.status = status
        self.detail = detail
        self.retry_after = retry_after


@dataclass(frozen=True)
class Provider:
    name: str
    model: str
    api_key: str = ""
    base_url: str = ""


@dataclass
class Result:
    data: Any
    provider: str
    model: str
    attempts: int
    notes: list[str]


def configured_providers(
    env: dict[str, str], order: list[str] | None = None
) -> tuple[list[Provider], list[str]]:
    """Providers that have what they need, plus a reason for each one skipped."""
    names = order or [
        n.strip().lower()
        for n in env.get("FRAMESMITH_LLM_PROVIDERS", DEFAULT_ORDER).split(",")
        if n.strip()
    ]
    providers: list[Provider] = []
    skipped: list[str] = []
    for name in names:
        if name not in KNOWN_PROVIDERS:
            skipped.append(f"{name}: unknown provider")
            continue
        prefix = f"FRAMESMITH_{name.upper()}"
        key = env.get(f"{prefix}_API_KEY", "").strip()
        model = env.get(f"{prefix}_MODEL", "").strip()
        if name in NEEDS_KEY and not key:
            skipped.append(f"{name}: no API key")
        elif not model:
            skipped.append(f"{name}: no model name (set {prefix}_MODEL)")
        else:
            base = ""
            if name == "ollama":
                base = env.get("FRAMESMITH_OLLAMA_URL", OLLAMA_DEFAULT_URL).rstrip("/")
            providers.append(Provider(name, model, key, base))
    return providers, skipped


def extract_json(text: str) -> Any:
    """Parse a JSON object from model text, tolerating code fences and surrounding prose."""
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("no JSON object found in the reply")
    try:
        return json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON ({exc.msg})") from exc


def _retry_after(value: str | None) -> float | None:
    try:
        return min(float(value), 60.0) if value else None
    except ValueError:
        return None


def _post(client: httpx.Client, url: str, headers: dict[str, str], body: dict) -> Any:
    response = client.post(url, headers=headers, json=body)
    if response.status_code >= 400:
        raise ProviderHTTPError(
            response.status_code,
            response.text[:160].replace("\n", " "),
            _retry_after(response.headers.get("retry-after")),
        )
    try:
        return response.json()
    except ValueError as exc:
        raise LLMError("provider reply was not JSON") from exc


def _messages(system: str, user: str) -> list[dict[str, str]]:
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def request_text(
    provider: Provider, system: str, user: str, client: httpx.Client, temperature: float
) -> str:
    """One call to one provider; returns the model's text."""
    try:
        if provider.name == "gemini":
            model = provider.model.removeprefix("models/")
            data = _post(
                client,
                GEMINI_URL.format(model=model),
                {"x-goog-api-key": provider.api_key},
                {
                    "systemInstruction": {"parts": [{"text": system}]},
                    "contents": [{"role": "user", "parts": [{"text": user}]}],
                    "generationConfig": {
                        "temperature": temperature,
                        "responseMimeType": "application/json",
                    },
                },
            )
            parts = data["candidates"][0]["content"]["parts"]
            text = "".join(p.get("text", "") for p in parts if not p.get("thought"))
        elif provider.name in ("openrouter", "opencode", "openai"):
            body: dict[str, Any] = {
                "model": provider.model,
                "messages": _messages(system, user),
                "temperature": temperature,
            }
            if provider.name == "openai":
                body["response_format"] = {"type": "json_object"}
                body["reasoning_effort"] = "none"
            url = {
                "openrouter": OPENROUTER_URL,
                "opencode": OPENCODE_URL,
                "openai": OPENAI_URL,
            }[provider.name]
            data = _post(client, url, {"Authorization": f"Bearer {provider.api_key}"}, body)
            text = data["choices"][0]["message"]["content"] or ""
        else:  # ollama
            data = _post(
                client,
                f"{provider.base_url}/api/chat",
                {},
                {
                    "model": provider.model,
                    "messages": _messages(system, user),
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": temperature},
                },
            )
            text = data["message"]["content"] or ""
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMError(f"unexpected {provider.name} reply shape") from exc
    if not text.strip():
        raise LLMError(f"{provider.name} returned an empty reply")
    return text


def _redact(text: str, secrets: list[str]) -> str:
    for secret in secrets:
        if secret:
            text = text.replace(secret, "***")
    return text


def generate_json(
    system: str,
    user: str,
    check: Check,
    env: dict[str, str],
    *,
    order: list[str] | None = None,
    client: httpx.Client | None = None,
    sleep: Callable[[float], None] = time.sleep,
    temperature: float = 0.9,
) -> Result:
    """Ask for JSON; validate with `check`; retry with feedback; fall back to the next provider."""
    providers, notes = configured_providers(env, order)
    if not providers:
        raise LLMError("no usable LLM provider: " + "; ".join(notes))
    try:
        retries = max(1, int(env.get("FRAMESMITH_LLM_MAX_RETRIES") or 3))
    except ValueError:
        retries = 3

    secrets = [p.api_key for p in providers]
    owns_client = client is None
    http = client or httpx.Client(timeout=180.0)
    made = 0
    try:
        for provider in providers:
            feedback = ""
            for attempt in range(1, retries + 1):
                made += 1
                tag = f"{provider.name} attempt {attempt}"
                try:
                    text = request_text(provider, system, user + feedback, http, temperature)
                except ProviderHTTPError as exc:
                    detail = _redact(exc.detail, secrets)
                    notes.append(f"{tag}: HTTP {exc.status} {detail}".strip())
                    if exc.status in RETRYABLE_STATUS and attempt < retries:
                        sleep(exc.retry_after or min(2**attempt, 30))
                        continue
                    break
                except httpx.HTTPError as exc:
                    notes.append(f"{tag}: network error {type(exc).__name__}")
                    if attempt < retries:
                        sleep(min(2**attempt, 30))
                        continue
                    break
                except LLMError as exc:
                    notes.append(f"{tag}: {exc}")
                    continue

                try:
                    data = extract_json(text)
                except ValueError as exc:
                    data, problems = None, [f"the reply was not valid JSON: {exc}"]
                else:
                    data, problems = check(data)
                if not problems:
                    return Result(data, provider.name, provider.model, made, notes)
                notes.append(f"{tag}: rejected ({len(problems)} problem(s): {problems[0]})")
                feedback = (
                    "\n\nYour previous answer was rejected for these reasons:\n- "
                    + "\n- ".join(problems[:8])
                    + "\nReturn corrected JSON only."
                )
    finally:
        if owns_client:
            http.close()
    raise LLMError("all providers failed: " + "; ".join(notes))
