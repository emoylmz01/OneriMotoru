"""
Notion'da Icerikler veritabani olusturma ve ornek veri ekleme scripti.
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("NOTION_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 1. AI project sayfasini bul
print("=== Notion workspace taraniyor... ===")
r = requests.post(
    "https://api.notion.com/v1/search",
    headers=HEADERS,
    json={"query": "AI project"}
)
print("Search status:", r.status_code)
data = r.json()

page_id = None
for obj in data.get("results", []):
    obj_type = obj.get("object")
    oid = obj.get("id", "")
    if obj_type == "page":
        props = obj.get("properties", {})
        title_prop = props.get("title", {})
        title_arr = title_prop.get("title", [])
        title = title_arr[0]["plain_text"] if title_arr else "Bilimiyor"
        print(f"  PAGE: {oid} | {title}")
        if not page_id:
            page_id = oid
    elif obj_type == "database":
        title_arr = obj.get("title", [])
        title = title_arr[0]["plain_text"] if title_arr else "Bilimiyor"
        print(f"  DB  : {oid} | {title}")
        if not page_id:
            page_id = oid  # DB parent olarak da kullanabiliriz

if not page_id:
    print("\nERROR: Erisebilecegimiz sayfa yok.")
    print("Not: 'AI project' sayfasina integrationu bagladin mi?")
    exit(1)

print(f"\nParent page ID: {page_id}")

# 2. Icerikler veritabanini olustur
print("\n=== 'Icerikler' veritabani olusturuluyor... ===")
db_payload = {
    "parent": {"type": "page_id", "page_id": page_id},
    "title": [{"type": "text", "text": {"content": "Icerikler"}}],
    "properties": {
        "Baslik": {
            "title": {}
        },
        "Kategori": {
            "select": {
                "options": [
                    {"name": "Yazilim",   "color": "blue"},
                    {"name": "Teknoloji", "color": "purple"},
                    {"name": "Is Dunyasi","color": "green"},
                    {"name": "Bilim",     "color": "yellow"},
                    {"name": "Tasarim",   "color": "pink"},
                    {"name": "Guevenlik", "color": "red"},
                    {"name": "Veri",      "color": "orange"},
                ]
            }
        },
        "Aciklama": {
            "rich_text": {}
        },
        "Etiketler": {
            "multi_select": {
                "options": [
                    {"name": "python",        "color": "blue"},
                    {"name": "yapay zeka",    "color": "purple"},
                    {"name": "ml",            "color": "pink"},
                    {"name": "web",           "color": "green"},
                    {"name": "react",         "color": "yellow"},
                    {"name": "girisimcilik",  "color": "orange"},
                    {"name": "veri bilimi",   "color": "red"},
                    {"name": "blockchain",    "color": "gray"},
                    {"name": "guvenlik",      "color": "brown"},
                    {"name": "mobil",         "color": "default"},
                ]
            }
        },
        "Populerlik": {
            "number": {"format": "number"}
        }
    }
}

r = requests.post("https://api.notion.com/v1/databases", headers=HEADERS, json=db_payload)
print("DB olusturma status:", r.status_code)

if r.status_code not in (200, 201):
    print("HATA:", r.text)
    exit(1)

db_data = r.json()
content_db_id = db_data["id"]
print(f"Icerikler DB ID: {content_db_id}")

# 3. Ornek icerikler ekle
print("\n=== Ornek icerikler ekleniyor... ===")

items = [
    {
        "baslik": "Python ile Makine Ogrenmesi",
        "kategori": "Yazilim",
        "aciklama": "Scikit-learn ve TensorFlow ile ML projeleri gelistirme rehberi.",
        "etiketler": ["python", "ml", "yapay zeka"],
        "populerlik": 95
    },
    {
        "baslik": "Girisimcilik 101",
        "kategori": "Is Dunyasi",
        "aciklama": "Sifirdan startup kurmak isteyenler icin temel rehber.",
        "etiketler": ["girisimcilik"],
        "populerlik": 88
    },
    {
        "baslik": "React ile Modern Web Gelistirme",
        "kategori": "Yazilim",
        "aciklama": "React, Next.js ve Tailwind ile profesyonel web uygulamalari.",
        "etiketler": ["react", "web"],
        "populerlik": 92
    },
    {
        "baslik": "Uzay Bilimi ve Astrofizik",
        "kategori": "Bilim",
        "aciklama": "Kara delikler, notron yildizlari ve evrenin genislemesi.",
        "etiketler": [],
        "populerlik": 74
    },
    {
        "baslik": "Yapay Zeka ve Etik",
        "kategori": "Teknoloji",
        "aciklama": "AI sistemlerinin toplum uzerindeki etkileri ve etik sorunlar.",
        "etiketler": ["yapay zeka"],
        "populerlik": 85
    },
    {
        "baslik": "Veri Bilimi ile Karar Verme",
        "kategori": "Veri",
        "aciklama": "Pandas, NumPy ve gorsellestirme ile veri analizi.",
        "etiketler": ["python", "veri bilimi"],
        "populerlik": 90
    },
    {
        "baslik": "Dijital Pazarlama Stratejileri",
        "kategori": "Is Dunyasi",
        "aciklama": "SEO, sosyal medya ve icerik pazarlama teknikleri.",
        "etiketler": ["girisimcilik"],
        "populerlik": 78
    },
    {
        "baslik": "Flutter ile Mobil Uygulama",
        "kategori": "Yazilim",
        "aciklama": "Flutter ve Dart ile cross-platform mobil uygulama gelistirme.",
        "etiketler": ["mobil"],
        "populerlik": 88
    },
    {
        "baslik": "Blockchain Temelleri",
        "kategori": "Teknoloji",
        "aciklama": "Kripto, akilli kontratlar ve dagitik sistemler.",
        "etiketler": ["blockchain"],
        "populerlik": 71
    },
    {
        "baslik": "Siber Guvenlik Rehberi",
        "kategori": "Guevenlik",
        "aciklama": "Penetrasyon testi, ag guvenligi ve etik hacking.",
        "etiketler": ["guvenlik"],
        "populerlik": 82
    },
    {
        "baslik": "UI/UX Tasarim Ilkeleri",
        "kategori": "Tasarim",
        "aciklama": "Figma ile kullanici odakli arayuz tasarimi ve prototipleme.",
        "etiketler": ["web"],
        "populerlik": 87
    },
    {
        "baslik": "FastAPI ile Backend Gelistirme",
        "kategori": "Yazilim",
        "aciklama": "Python FastAPI, async programlama ve REST API tasarimi.",
        "etiketler": ["python", "web"],
        "populerlik": 89
    },
]

for item in items:
    # Etiketler -> multi_select format
    etiket_objs = [{"name": e} for e in item["etiketler"]]

    page_payload = {
        "parent": {"database_id": content_db_id},
        "properties": {
            "Baslik": {
                "title": [{"text": {"content": item["baslik"]}}]
            },
            "Kategori": {
                "select": {"name": item["kategori"]}
            },
            "Aciklama": {
                "rich_text": [{"text": {"content": item["aciklama"]}}]
            },
            "Etiketler": {
                "multi_select": etiket_objs
            },
            "Populerlik": {
                "number": item["populerlik"]
            }
        }
    }

    r = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=page_payload)
    status = "OK" if r.status_code in (200, 201) else f"HATA {r.status_code}"
    print(f"  [{status}] {item['baslik']}")

# 4. .env guncelle
print("\n=== .env guncelleniyor... ===")
env_path = ".env"
with open(env_path, "r") as f:
    env_content = f.read()

if "NOTION_CONTENT_DATABASE_ID" in env_content:
    # Guncelle
    lines = env_content.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("NOTION_CONTENT_DATABASE_ID"):
            new_lines.append(f"NOTION_CONTENT_DATABASE_ID={content_db_id}")
        else:
            new_lines.append(line)
    env_content = "\n".join(new_lines)
else:
    env_content = env_content.rstrip() + f"\nNOTION_CONTENT_DATABASE_ID={content_db_id}\n"

with open(env_path, "w") as f:
    f.write(env_content)

print(f"NOTION_CONTENT_DATABASE_ID={content_db_id} -> .env'e yazildi")
print("\n=== Tum islemler tamamlandi! ===")
print(f"Icerikler DB: https://notion.so/{content_db_id.replace('-', '')}")
