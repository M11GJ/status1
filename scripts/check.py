#!/usr/bin/env python3
"""DCC AI ステータスチェッカー。対象URLを叩いて data/history.json に追記する。"""
import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

TARGETS = {
    "ai": "https://ai.shu-dcc.net/api/config",
    "usage": "https://usage.shu-dcc.net/",
}
# usage は未ログイン時 302 リダイレクトが正常系
OK_STATUSES = {"ai": {200}, "usage": {200, 302}}

HISTORY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "history.json")
RETENTION_DAYS = 90
TIMEOUT = 10


def check(name, url):
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "dcc-status-checker"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = resp.status
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception:
        status = 0
    ms = round((time.time() - start) * 1000)
    ok = status in OK_STATUSES.get(name, {200})
    return {"ok": ok, "status": status, "ms": ms}


def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"checks": []}


def save_history(data):
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def prune(data):
    cutoff = time.time() - RETENTION_DAYS * 86400
    data["checks"] = [
        c for c in data["checks"]
        if datetime.fromisoformat(c["ts"].replace("Z", "+00:00")).timestamp() >= cutoff
    ]


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    targets_result = {name: check(name, url) for name, url in TARGETS.items()}

    data = load_history()
    data["checks"].append({"ts": now, "targets": targets_result})
    prune(data)
    save_history(data)

    print(json.dumps({"ts": now, "targets": targets_result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
