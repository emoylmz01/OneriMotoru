import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# The page ID that we know exists
PAGE_ID = "67ba2e22650c46cc981d8c3335f8b2c2"

print("Creating Kullanicilar Database...")
db_payload = {
    "parent": {"type": "page_id", "page_id": PAGE_ID},
    "title": [{"type": "text", "text": {"content": "Kullanicilar"}}],
    "properties": {
        "Name": {
            "title": {}
        },
        "Interest": {
            "rich_text": {}
        }
    }
}

r = requests.post("https://api.notion.com/v1/databases", headers=HEADERS, json=db_payload)
if r.status_code not in (200, 201):
    print("Error:", r.text)
    exit(1)

db_id = r.json()["id"]
print("Kullanicilar DB ID:", db_id)

# Update .env
env_path = ".env"
with open(env_path, "r") as f:
    env_content = f.read()

lines = env_content.splitlines()
new_lines = []
for line in lines:
    if line.startswith("NOTION_DATABASE_ID"):
        new_lines.append(f"NOTION_DATABASE_ID={db_id}")
    else:
        new_lines.append(line)

with open(env_path, "w") as f:
    f.write("\n".join(new_lines) + "\n")

print("Updated .env with NOTION_DATABASE_ID")
