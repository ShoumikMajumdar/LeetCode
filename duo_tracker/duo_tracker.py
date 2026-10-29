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
import argparse, json, math, random, sys, time, urllib.parse, urllib.request

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
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


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
    link = "https://www.apple.com/shop/product/" + part
    req = urllib.request.Request(
        "https://ntfy.sh/" + topic, method="POST",
        data=f"{title or 'iPhone Duo ' + storage + ' ' + color} in stock at {store} - GO".encode(),
        headers={"Title": "DUO IN STOCK", "Priority": "5", "Tags": "rotating_light", "Click": link})
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        emit("ntfy_error", error=str(e))


def poll(parts, seen, topic):
    for z in SEED_ZIPS:
        try:
            resp = fetch(z, parts)
        except Exception as e:
            emit("fetch_error", zip=z, error=str(e)[:120])
            continue
        for s, part, title in available(resp, parts):
            if not in_range(s):
                continue
            key = (s.get("storeNumber"), part)
            if key in seen:
                continue
            seen.add(key)
            storage, color, price = SKUS[part]
            emit("IN_STOCK", store=s.get("storeName"), city=s.get("city"), state=s.get("state"),
                 store_id=s.get("storeNumber"), part=part, model=f"iPhone Duo {storage} {color}",
                 price=price, link="https://www.apple.com/shop/product/" + part)
            if topic:
                ntfy(topic, s.get("storeName"), part, title)
        # Anything previously seen but no longer available can alert again next restock.
        live = {(s.get("storeNumber"), p) for s, p, _ in available(resp, parts)}
        stores_here = {s.get("storeNumber") for s in
                       (((resp.get("body") or {}).get("content") or {}).get("pickupMessage") or {}).get("stores") or []}
        for k in [k for k in seen if k[0] in stores_here and k not in live]:
            seen.discard(k)
            emit("SOLD_OUT", store_id=k[0], part=k[1])


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
    emit = lambda kind, **kw: out.append((kind, kw.get("store_id")))
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
    ap.add_argument("--interval", type=float, default=6, help="seconds between sweeps (default 6)")
    ap.add_argument("--ntfy", help="optional ntfy.sh topic for direct phone push")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    parts = [p for p, (st, co, _) in SKUS.items()
             if (not a.storage or st.lower() == a.storage.lower()) and (not a.color or co.lower() == a.color.lower())]
    if not parts:
        sys.exit("no SKU matches those filters")
    emit("started", watching=parts, zips=SEED_ZIPS, interval=a.interval)
    seen = set()
    while True:
        poll(parts, seen, a.ntfy)
        time.sleep(a.interval * random.uniform(0.8, 1.2))


if __name__ == "__main__":
    main()
