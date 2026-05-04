"""
Notion API servisi — Kullanıcı ve içerik veritabanı işlemleri.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# ──────────────────────────────────────────────
# Kullanıcı İşlemleri
# ──────────────────────────────────────────────

def add_user(name: str, interest: str):
    """Notion'a yeni kullanıcı ekler."""
    url = "https://api.notion.com/v1/pages"

    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": name}}
                ]
            },
            "Interest": {
                "rich_text": [
                    {"text": {"content": interest}}
                ]
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()


def get_all_users():
    """Notion'daki tüm kullanıcıları çeker."""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers, json={})

    if response.status_code != 200:
        return {"error": response.text}

    results = response.json().get("results", [])
    users = []
    for page in results:
        props = page.get("properties", {})
        name = ""
        interest = ""

        # Name alanını çek
        name_prop = props.get("Name", {})
        if name_prop.get("title"):
            name = name_prop["title"][0]["text"]["content"]

        # Interest alanını çek
        interest_prop = props.get("Interest", {})
        if interest_prop.get("rich_text"):
            interest = interest_prop["rich_text"][0]["text"]["content"]

        users.append({
            "id": page["id"],
            "name": name,
            "interest": interest
        })

    return users


# ──────────────────────────────────────────────
# İçerik İşlemleri (Eğer ayrı bir İçerikler DB varsa)
# ──────────────────────────────────────────────

CONTENT_DATABASE_ID = os.getenv("NOTION_CONTENT_DATABASE_ID")


def get_all_items():
    """
    Notion'daki içerik/ürün tablosundan tüm öğeleri çeker.
    Eğer ayrı bir içerik DB yoksa, boş bir örnek set döner.
    """
    if not CONTENT_DATABASE_ID:
        # İçerik DB yoksa demo veri döndür
        return _get_demo_items()

    url = f"https://api.notion.com/v1/databases/{CONTENT_DATABASE_ID}/query"
    response = requests.post(url, headers=headers, json={})

    if response.status_code != 200:
        return _get_demo_items()

    results = response.json().get("results", [])
    items = []
    for page in results:
        props = page.get("properties", {})

        title = ""
        title_prop = props.get("Baslik", props.get("Name", {}))
        if title_prop.get("title"):
            title = title_prop["title"][0]["text"]["content"]

        category = ""
        cat_prop = props.get("Kategori", props.get("Category", {}))
        if cat_prop.get("select"):
            category = cat_prop["select"]["name"]

        description = ""
        desc_prop = props.get("Aciklama", props.get("Description", {}))
        if desc_prop.get("rich_text"):
            description = desc_prop["rich_text"][0]["text"]["content"]

        tags = []
        tags_prop = props.get("Etiketler", props.get("Tags", {}))
        if tags_prop.get("multi_select"):
            tags = [t["name"] for t in tags_prop["multi_select"]]

        items.append({
            "id": page["id"],
            "title": title,
            "category": category,
            "description": description,
            "tags": tags
        })

    return items


def _get_demo_items():
    """İçerik DB yoksa kullanılacak demo veri seti."""
    return [
        {"id": "demo-1", "title": "Python ile Makine Öğrenmesi",
         "category": "Yazılım", "description": "Scikit-learn ve TensorFlow ile ML projeleri geliştirme rehberi.",
         "tags": ["python", "ml", "yapay zeka"]},

        {"id": "demo-2", "title": "Girişimcilik 101",
         "category": "İş Dünyası", "description": "Sıfırdan startup kurmak isteyenler için temel rehber.",
         "tags": ["girişimcilik", "startup", "iş"]},

        {"id": "demo-3", "title": "React ile Modern Web Geliştirme",
         "category": "Yazılım", "description": "React, Next.js ve Tailwind ile profesyonel web uygulamaları.",
         "tags": ["react", "frontend", "web"]},

        {"id": "demo-4", "title": "Uzay Bilimi ve Astrofizik",
         "category": "Bilim", "description": "Kara delikler, nötron yıldızları ve evrenin genişlemesi.",
         "tags": ["uzay", "bilim", "fizik"]},

        {"id": "demo-5", "title": "Yapay Zeka ve Etik",
         "category": "Teknoloji", "description": "AI sistemlerinin toplum üzerindeki etkileri ve etik sorunlar.",
         "tags": ["yapay zeka", "etik", "teknoloji"]},

        {"id": "demo-6", "title": "Veri Bilimi ile Karar Verme",
         "category": "Veri", "description": "Pandas, NumPy ve görselleştirme ile veri analizi.",
         "tags": ["veri bilimi", "python", "analiz"]},

        {"id": "demo-7", "title": "Dijital Pazarlama Stratejileri",
         "category": "Pazarlama", "description": "SEO, sosyal medya ve içerik pazarlama teknikleri.",
         "tags": ["pazarlama", "dijital", "seo"]},

        {"id": "demo-8", "title": "Mobil Uygulama Geliştirme",
         "category": "Yazılım", "description": "Flutter ve React Native ile cross-platform uygulama.",
         "tags": ["mobil", "flutter", "uygulama"]},

        {"id": "demo-9", "title": "Blockchain Temelleri",
         "category": "Teknoloji", "description": "Kripto, akıllı kontratlar ve dağıtık sistemler.",
         "tags": ["blockchain", "kripto", "teknoloji"]},

        {"id": "demo-10", "title": "Siber Güvenlik Rehberi",
         "category": "Güvenlik", "description": "Penetrasyon testi, ağ güvenliği ve etik hacking.",
         "tags": ["güvenlik", "hacking", "siber"]},
    ]


# ──────────────────────────────────────────────
# Feedback İşlemleri
# ──────────────────────────────────────────────

def save_feedback(user_name: str, item_title: str, feedback: str):
    """
    Kullanıcının bir içeriğe verdiği feedback'i Notion'a kaydeder.
    Kullanıcılar DB'sine yeni bir satır ekler (basit loglama).
    """
    url = "https://api.notion.com/v1/pages"

    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {"text": {"content": f"[FEEDBACK] {user_name}"}}
                ]
            },
            "Interest": {
                "rich_text": [
                    {"text": {"content": f"{feedback}: {item_title}"}}
                ]
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)
    return {
        "status": "saved" if response.status_code == 200 else "error",
        "user": user_name,
        "item": item_title,
        "feedback": feedback
    }