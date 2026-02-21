import json, os, time, urllib.request, urllib.error

def call_llm(system: str, user: str, model: str = "claude-sonnet-4-5", max_tokens: int = 10024) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    payload = json.dumps({
        "model": model,
        "max_tokens": max_tokens,
        "temperature": 0.7,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=320) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["content"][0]["text"]
        usage = data.get("usage", {})
        debug_line = (
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"model={data.get('model', '?')} "
            f"in={usage.get('input_tokens', '?')} "
            f"out={usage.get('output_tokens', '?')} "
            f"stop={data.get('stop_reason', '?')} "
            f"preview={repr(content[:80])}\n"
        )
        with open("/tmp/oc-llm-debug.log", "a", encoding="utf-8") as f:
            f.write(debug_line)
        return content
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Anthropic API error {e.code}: {e.read().decode()}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Anthropic API error: {e}") from e
