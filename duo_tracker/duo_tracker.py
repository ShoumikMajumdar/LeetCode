#!/usr/bin/env python3
"""iPhone Duo pickup-stock tracker for Apple Stores near Brighton, MA (MA + NH, 45 mi).

Same data source InStock Radar uses: Apple's public pickup-availability endpoint
(www.apple.com/shop/fulfillment-messages). Stdlib only.

Output: one JSON object per line on stdout. Run it under Claude's Monitor tool and
each IN_STOCK line wakes Claude, who pushes the notification. --ntfy additionally
posts straight to your phone (faster; no LLM in the loop).

    python3 duo_tracker.py                      # watch everything, 8 SKUs
    python3 duo_tracker.py --storage 512GB --color "Night Sky" --ntfy my-secret-topic
    python3 duo_tracker.py --selftest
"""
import argparse, json, math, random, sys, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

HOME = (42.3464, -71.1627)  # Brighton, Boston
RADIUS_MI = 45
STATES = {"MA", "NH"}
# Seed ZIPs: Apple returns only the nearest few stores per query, so union several.
SEED_ZIPS = ["02135", "01701", "01887", "01840", "03079", "03060", "02360", "01545"]

# US SKUs, scraped from apple.com/shop/buy-iphone/iphone-duo
SKUS = {
    "MK1E4LL/A": ("256GB", "Star White", 1999), "MK1F4LL/A": ("256GB", "Night Sky", 1999),
    "MK1G4LL/A": ("512GB", "Star White", 2199), "MK1H4LL/A": ("512GB", "Night Sky", 2199),
    "MK1J4LL/A": ("1TB", "Star White", 2599),   "MK1L4LL/A": ("1TB", "Night Sky", 2599),
    "MK1Q4LL/A": ("2TB", "Star White", 3199),   "MK1R4LL/A": ("2TB", "Night Sky", 3199),
}
ENDPOINT = "https://www.apple.com/shop/fulfillment-messages"
UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 19_0 like Mac OS X) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/19.0 Mobile/15E148 Safari/604.1")


def miles(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 3958.8 * 2 * math.asin(math.sqrt(h))


def fetch(zip_code, parts):
    q = [("pl", "true"), ("mts.0", "regular"), ("mts.1", "sticky"), ("fts", "true"),
         ("location", zip_code)] + [(f"parts.{i}", p) for i, p in enumerate(parts)]
    req = urllib.request.Request(ENDPOINT + "?" + urllib.parse.urlencode(q),
                                 headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read()
    except urllib.error.HTTPError as e:
        if e.code in BLOCK_CODES:
            raise Blocked(f"HTTP {e.code}")
        raise
    try:
        return json.loads(body)
    except ValueError:  # an HTML error / challenge page instead of JSON
        raise Blocked("non-JSON response")


class Blocked(Exception):
    """Apple is refusing or throttling us (as opposed to a network blip)."""


BLOCK_CODES = {403, 429, 503, 541}


def available(resp, parts):
    """Yield (store_dict, part, title) for every in-stock pickup in the response."""
    stores = (((resp.get("body") or {}).get("content") or {}).get("pickupMessage") or {}).get("stores") or []
    for s in stores:
        pa = s.get("partsAvailability") or {}
        for part in parts:
            info = pa.get(part) or {}
            # "available" only; "unavailable" / "ineligible" must not match.
            if str(info.get("pickupDisplay", "")).lower() == "available":
                title = (info.get("messageTypes", {}).get("regular", {}) or {}).get("storePickupProductTitle")
                yield s, part, title


def in_range(s):
    if (s.get("state") or "").upper() not in STATES and s.get("state"):
        return False
    lat, lon = s.get("latitude"), s.get("longitude")
    if lat is None or lon is None:  # coordinates absent: trust the state filter
        return True
    return miles(HOME, (float(lat), float(lon))) <= RADIUS_MI


def emit(kind, **kw):
    print(json.dumps({"event": kind, "ts": time.strftime("%H:%M:%S"), **kw}), flush=True)


def ntfy(topic, store, part, title):
    storage, color, price = SKUS[part]
    push(topic, "DUO IN STOCK", f"{title or 'iPhone Duo ' + storage + ' ' + color} in stock at {store} - GO",
         priority="5", tags="rotating_light", click="https://www.apple.com/shop/product/" + part)


def push(topic, title, msg, priority="3", tags="", click=None):
    headers = {"Title": title, "Priority": priority, "Tags": tags}
    if click:
        headers["Click"] = click
    req = urllib.request.Request("https://ntfy.sh/" + topic, method="POST", data=msg.encode(), headers=headers)
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        emit("ntfy_error", error=str(e))


POOL = ThreadPoolExecutor(max_workers=16)


def _fetch_one(z, parts, blocked):
    try:
        return fetch(z, parts)
    except Blocked as e:
        blocked.append(str(e))
        emit("blocked", zip=z, error=str(e))
        return None
    except Exception as e:
        emit("fetch_error", zip=z, error=str(e)[:120])
        return None


def poll(parts, seen, topic):
    """One sweep: query every seed ZIP in parallel, merge, then diff against the last sweep."""
    t0 = time.monotonic()
    blocked = []
    resps = [r for r in POOL.map(lambda z: _fetch_one(z, parts, blocked), SEED_ZIPS) if r]
    live, checked, hits = set(), set(), {}
    for resp in resps:
        for s in (((resp.get("body") or {}).get("content") or {}).get("pickupMessage") or {}).get("stores") or []:
            checked.add(s.get("storeNumber"))
        for s, part, title in available(resp, parts):
            if in_range(s):
                key = (s.get("storeNumber"), part)
                live.add(key)
                hits.setdefault(key, (s, title))
    for key in live - seen:
        s, title = hits[key]
        part = key[1]
        if topic:  # push first, off-thread: nothing below may delay the phone
            POOL.submit(ntfy, topic, s.get("storeName"), part, title)
        storage, color, price = SKUS[part]
        emit("IN_STOCK", store=s.get("storeName"), city=s.get("city"), state=s.get("state"),
             store_id=key[0], part=part, model=f"iPhone Duo {storage} {color}", price=price,
             link="https://www.apple.com/shop/product/" + part,
             detect_ms=round((time.monotonic() - t0) * 1000))
    # Only clear stores this sweep actually saw, so a failed request can't fake a restock.
    for key in [k for k in seen if k[0] in checked and k not in live]:
        emit("SOLD_OUT", store_id=key[0], part=key[1])
    seen.difference_update({k for k in seen if k[0] in checked} - live)
    seen.update(live)
    return bool(blocked)


def store_ids(resp):
    return {s.get("storeNumber") for s in
            (((resp.get("body") or {}).get("content") or {}).get("pickupMessage") or {}).get("stores") or []
            if in_range(s)}


def trim_zips(parts):
    """Ask each seed ZIP once, slowly, then keep the fewest ZIPs that still cover every in-range store.
    Fewer ZIPs = fewer requests per sweep = less chance Apple throttles us."""
    cover = {}
    for z in SEED_ZIPS:
        try:
            cover[z] = store_ids(fetch(z, parts))
        except Exception as e:
            emit("discover_error", zip=z, error=str(e)[:120])
        time.sleep(1.5)
    if not cover:
        return SEED_ZIPS
    todo, keep = set().union(*cover.values()), []
    while todo:
        z = max(cover, key=lambda k: len(cover[k] & todo))
        keep.append(z)
        todo -= cover[z]
    emit("discovered", stores=sorted(set().union(*cover.values())), zips=keep)
    return keep or SEED_ZIPS


def selftest():
    fixture = {"body": {"content": {"pickupMessage": {"stores": [
        {"storeNumber": "R001", "storeName": "Test Boylston", "city": "Boston", "state": "MA",
         "latitude": 42.35, "longitude": -71.07, "partsAvailability": {
             "MK1F4LL/A": {"pickupDisplay": "available",
                           "messageTypes": {"regular": {"storePickupProductTitle": "iPhone Duo 256GB Night Sky"}}},
             "MK1E4LL/A": {"pickupDisplay": "unavailable"}}},
        {"storeNumber": "R002", "storeName": "Far Away", "city": "Hartford", "state": "CT",
         "partsAvailability": {"MK1F4LL/A": {"pickupDisplay": "available"}}},
        {"storeNumber": "R003", "storeName": "Too Far MA", "city": "Pittsfield", "state": "MA",
         "latitude": 42.45, "longitude": -73.25, "partsAvailability": {"MK1F4LL/A": {"pickupDisplay": "available"}}},
    ]}}}}
    global fetch, SEED_ZIPS
    SEED_ZIPS = ["02135"]
    calls = {"n": 0}

    def fake(zip_code, parts):
        calls["n"] += 1
        if calls["n"] == 3:  # third poll: Boylston sells out
            fixture["body"]["content"]["pickupMessage"]["stores"][0]["partsAvailability"]["MK1F4LL/A"]["pickupDisplay"] = "unavailable"
        if calls["n"] == 4:  # fourth: restock -> must alert again
            fixture["body"]["content"]["pickupMessage"]["stores"][0]["partsAvailability"]["MK1F4LL/A"]["pickupDisplay"] = "available"
        return fixture
    fetch = fake
    seen, out = set(), []
    global emit
    real = emit
    emit = lambda kind, **kw: out.append((kind, kw.get("store_id"))) if kind in ("IN_STOCK", "SOLD_OUT") else None
    for _ in range(4):
        poll(list(SKUS), seen, None)
    emit = real
    assert out == [("IN_STOCK", "R001"), ("SOLD_OUT", "R001"), ("IN_STOCK", "R001")], out
    assert 40 < miles(HOME, (42.45, -73.25)) and miles(HOME, (42.45, -73.25)) > RADIUS_MI
    print("selftest ok:", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--storage", help="256GB|512GB|1TB|2TB")
    ap.add_argument("--color", help='"Night Sky" or "Star White"')
    ap.add_argument("--interval", type=float, default=5, help="seconds between sweeps (default 5)")
    ap.add_argument("--ntfy", help="optional ntfy.sh topic for direct phone push")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    parts = [p for p, (st, co, _) in SKUS.items()
             if (not a.storage or st.lower() == a.storage.lower()) and (not a.color or co.lower() == a.color.lower())]
    if not parts:
        sys.exit("no SKU matches those filters")
    global SEED_ZIPS
    SEED_ZIPS = trim_zips(parts)
    emit("started", watching=parts, zips=SEED_ZIPS, interval=a.interval)
    seen, delay, paused_at = set(), a.interval, None
    while True:
        if poll(parts, seen, a.ntfy):
            # Throttled: double the gap (cap 10 min) and tell the phone once, so you never think
            # it's watching while it isn't.
            delay = min(delay * 2, 600)
            if paused_at is None:
                paused_at = time.time()
                if a.ntfy:
                    push(a.ntfy, "Duo tracker throttled", "Apple is refusing requests. Backing off; "
                         "NOT watching reliably until it recovers.", priority="4", tags="warning")
            emit("backoff", next_sweep_s=delay)
        else:
            if paused_at is not None:
                if a.ntfy:
                    push(a.ntfy, "Duo tracker back", f"Watching again after {round((time.time() - paused_at) / 60)} min.")
                paused_at = None
            delay = max(a.interval, delay / 2)  # ease back to normal speed, don't snap back
        time.sleep(delay * random.uniform(0.8, 1.2))


if __name__ == "__main__":
    main()
