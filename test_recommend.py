"""Test: AI Oneri Motoru"""
import requests
import json

# 1. Root test
r = requests.get("http://127.0.0.1:8000/")
print("=== ROOT ===")
print("Status:", r.status_code)

# 2. Items test
r = requests.get("http://127.0.0.1:8000/items")
data = r.json()
print("\n=== ITEMS ===")
print("Count:", data["count"])
for item in data["items"][:3]:
    print(f"  - {item['title']} [{item['category']}]")

# 3. Smart Recommend test (ANA OLAY)
print("\n=== AI ONERI (yapay zeka ve yazilim) ===")
r = requests.post("http://127.0.0.1:8000/recommend", json={
    "interest": "yapay zeka ve yazilim",
    "history": []
})
data = r.json()
print("Analyzed items:", data.get("total_items_analyzed"))
recs = data.get("recommendations", {})
if isinstance(recs, dict):
    for model, model_recs in recs.items():
        print(f"\n  --- {model} ---")
        for rec in model_recs:
            title = rec.get("title", "?")
            score = rec.get("score", 0)
            reason = rec.get("reason", "")
            print(f"  [{score}%] {title}")
            print(f"        -> {reason}")
else:
    print("  Error:", recs)


# 4. Feedback test
print("\n=== FEEDBACK ===")
r = requests.post("http://127.0.0.1:8000/feedback", json={
    "user_name": "Test Kullanici",
    "item_title": "Python ile Makine Ogrenmesi",
    "feedback": "like"
})
print("Feedback:", r.json())

print("\n=== TAMAMLANDI ===")
