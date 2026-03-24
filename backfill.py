import json
import os
from datetime import date

LOG_FILE = "recommendations_log.json"

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        log = json.load(f)
else:
    log = []

print("── Backfill old recommendations ─────────────────")
print("Enter details for each run you want to add.")
print("Press Enter with no ticker to finish.\n")

while True:
    ticker = input("Ticker (e.g. ANET, VRT): ").strip().upper()
    if not ticker:
        break

    run_date = input(f"Run date (YYYY-MM-DD) [default: {date.today()}]: ").strip()
    if not run_date:
        run_date = date.today().strftime("%Y-%m-%d")

    print("Verdict options: BUY / HOLD / SELL")
    verdict = input("Verdict: ").strip().upper()
    if verdict not in ["BUY", "HOLD", "SELL"]:
        verdict = "UNKNOWN"

    analysis = input("Paste a short summary (or press Enter to skip): ").strip()

    analysts = input("Analysts used [default: market,fundamentals,silicon_valley]: ").strip()
    if not analysts:
        analysts = "market,fundamentals,silicon_valley"
    analysts_list = [a.strip() for a in analysts.split(",")]

    record = {
        "ticker":        ticker,
        "run_date":      run_date,
        "verdict":       verdict,
        "full_analysis": analysis,
        "config": {
            "analysts":      analysts_list,
            "debate_rounds": 1,
            "model":         "claude-haiku-4-5-20251001",
        },
        "review": {
            "review_date":     None,
            "price_at_run":    None,
            "price_at_review": None,
            "actual_outcome":  None,
            "was_correct":     None,
            "notes":           None,
        }
    }

    log.append(record)

    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    print(f"✓ Added {ticker} ({run_date}) — {verdict}\n")

print(f"\nDone! {LOG_FILE} now has {len(log)} records.")
print("Run python3 review.py to fill in the review fields.")
