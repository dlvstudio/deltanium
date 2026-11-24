#!/usr/bin/env python3
"""Uptime check for the public Deltanium endpoints (mainnet + testnet).

Prints one line per problem and exits 1 when anything is wrong. A check that fails is retried after a pause,
so a single slow request does not raise an alert. Only public URLs are used; no secrets are needed.
"""
import datetime, json, os, socket, ssl, sys, time, urllib.request

NODES = ["api", "store-1", "store-2", "blocker-1",
         "testnet-api", "testnet-store-1", "testnet-store-2", "testnet-blocker-1"]
PAGES = ["https://deltanium.com/", "https://app.deltanium.com/", "https://testnet-app.deltanium.com/"]
CENTRALS = ["api", "testnet-api"]
CERT_MIN_DAYS = 14
RETRY_PAUSE = 60


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "deltanium-uptime"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status, r.read()


def check_node(host):
    status, body = get(f"https://{host}.deltanium.com/api/version")
    v = json.loads(body)
    return f"{v.get('service')} {v.get('version')} {v.get('commitShort')} {v.get('network')}"


def check_page(url):
    status, _ = get(url)
    return f"HTTP {status}"


def check_central(host):
    _, body = get(f"https://{host}.deltanium.com/api/explorer/status")
    s = json.loads(body)
    active, reachable = s.get("activeBlockers", 0), s.get("reachableBlockers", 0)
    if reachable < 1:
        raise RuntimeError(f"no reachable block creator (active={active}, reachable={reachable})")
    return f"tipHeight={s.get('tipHeight')} blockers {reachable}/{active} reachable"


def check_cert(host):
    ctx = ssl.create_default_context()
    with socket.create_connection((host, 443), timeout=20) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as tls:
            not_after = tls.getpeercert()["notAfter"]
    expires = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
    days = (expires - datetime.datetime.utcnow()).days
    if days < CERT_MIN_DAYS:
        raise RuntimeError(f"TLS certificate expires in {days} days ({expires:%Y-%m-%d})")
    return f"cert ok, {days} days left"


def run_all():
    checks = [(f"{h}.deltanium.com /api/version", check_node, h) for h in NODES]
    checks += [(u, check_page, u) for u in PAGES]
    checks += [(f"{h}.deltanium.com blockers", check_central, h) for h in CENTRALS]
    hosts = [f"{h}.deltanium.com" for h in NODES] + ["deltanium.com", "app.deltanium.com", "testnet-app.deltanium.com"]
    checks += [(f"{h} TLS", check_cert, h) for h in hosts]
    if os.environ.get("SIMULATE_FAILURE"):
        checks.append(("simulated failure (manual test run)", check_page, "https://nonexistent.deltanium.com/"))
    ok, bad = [], {}
    for name, fn, arg in checks:
        try:
            ok.append(f"{name}: {fn(arg)}")
        except Exception as e:  # noqa: BLE001 - any failure is a finding
            bad[name] = (fn, arg, f"{type(e).__name__}: {e}")
    return ok, bad


def main():
    ok, bad = run_all()
    if bad:
        time.sleep(RETRY_PAUSE)
        still = {}
        for name, (fn, arg, _) in bad.items():
            try:
                ok.append(f"{name}: {fn(arg)} (after retry)")
            except Exception as e:  # noqa: BLE001
                still[name] = f"{type(e).__name__}: {e}"
        bad = still
    for line in ok:
        print("OK   " + line)
    for name, err in bad.items():
        print(f"FAIL {name}: {err}")
    with open("monitor-result.md", "w") as f:
        for name, err in bad.items():
            f.write(f"- **{name}**: {err}\n")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
