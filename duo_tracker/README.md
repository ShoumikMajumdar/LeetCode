# iPhone Duo tracker (MA + NH, 45 mi from Brighton)

Polls Apple's pickup-availability endpoint (the same source InStock Radar reads) for all 8 US
iPhone Duo SKUs, every ~4 s, all seed ZIPs in parallel. On a restock it pushes to your phone
directly via ntfy, before anything else happens.

## Setup (5 min)
1. Install **ntfy** on your iPhone, subscribe to a long random topic (anyone who knows it can post to it).
   In iOS Settings > Notifications > ntfy, allow Time Sensitive notifications.
2. Run once by hand to confirm Apple answers from your network:
   `python3 duo_tracker.py --ntfy YOUR-TOPIC` (Ctrl-C to stop). You should see `started` and no `fetch_error` lines.
3. Install as a service so it runs 24/7 and restarts itself: `com.duo.tracker.plist` (Mac) or
   `duo-tracker.service` (Linux / Raspberry Pi). Edit the paths and topic first.

Filter: `--storage 512GB --color "Night Sky"`. Speed: `--interval 5` is the default.

## If Apple throttles you
- At startup it checks each seed ZIP once and keeps only the fewest ZIPs that cover every store in range,
  so a sweep is usually 2-3 requests, not 8.
- A 403/429/503/541 or an HTML page instead of JSON counts as throttled: it doubles the wait (up to 10 min),
  pushes **"Duo tracker throttled"** to your phone, then eases back and pushes **"Duo tracker back"**.
- Blocks are on your IP address, not your Apple ID: buying still works from your phone on cellular.
- If you get throttled often, raise `--interval` (8-10 s still beats InStock Radar's 20 s).

## Ordering fast
Apple Store app signed in, Apple Pay default, pickup store picked. Tap the alert, then Reserve, then Face ID.

## Claude in the loop (optional, slower)
Each restock is also a JSON line on stdout. A Claude Code session running on the same machine can watch it with
the Monitor tool and send you a push, but that waits on a model turn: seconds you don't have
with 10-15 s windows. Use it for a summary, not as the alarm.
