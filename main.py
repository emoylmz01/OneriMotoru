"""
AI Öneri Motoru — Ana API (FastAPI)
=====================================
Endpoint'ler:
  GET  /              → Sistem durumu
  GET  /items          → İçerik listesi (Notion veya demo)
  GET  /users          → Kullanıcı listesi (Notion)
  POST /user           → Yeni kullanıcı ekle
  POST /recommend      → AI ile akıllı öneri al
  POST /feedback       → Kullanıcı geri bildirimi (👍/👎)
  GET  /recommend      → Basit öneri (geriye uyumlu)
  POST /zapier-webhook → Zapier entegrasyonu için webhook
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_service import get_recommendation, generate_smart_recommendations, simulate_recommendations, generate_item_details
from notion_service import add_user, get_all_users, get_all_items, save_feedback
from models import UserCreate, FeedbackRequest, RecommendRequest, ItemDetailRequest

app = FastAPI(
    title="AI Öneri Motoru",
    description="Kullanıcı davranışlarına göre akıllı öneri üreten sistem.",
    version="1.0.0"
)

# CORS — Frontend'den erişim için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Sistem
# ──────────────────────────────────────────────

@app.get("/", tags=["Sistem"])
def home():
    """Sistem durumu kontrolü."""
    return {
        "status": "çalışıyor ✅",
        "message": "AI Öneri Motoru aktif",
        "endpoints": ["/items", "/users", "/recommend", "/feedback"]
    }


# ──────────────────────────────────────────────
# İçerikler
# ──────────────────────────────────────────────

@app.get("/items", tags=["İçerikler"])
def list_items():
    """Notion'daki veya demo içerik havuzunu döner."""
    items = get_all_items()
    return {
        "count": len(items),
        "items": items
    }


# ──────────────────────────────────────────────
# Kullanıcılar
# ──────────────────────────────────────────────

@app.get("/users", tags=["Kullanıcılar"])
def list_users():
    """Notion'daki tüm kullanıcıları listeler."""
    users = get_all_users()
    return {
        "count": len(users) if isinstance(users, list) else 0,
        "users": users
    }


@app.post("/user", tags=["Kullanıcılar"])
def create_user(user: UserCreate):
    """Notion'a yeni kullanıcı ekler."""
    result = add_user(user.name, user.interest)
    return {
        "status": "created",
        "user": user.name,
        "interest": user.interest,
        "notion_response": result
    }


# ──────────────────────────────────────────────
# Öneri Motoru (ANA ÖZELLİK 🔥)
# ──────────────────────────────────────────────

@app.post("/recommend", tags=["Öneri Motoru"])
def smart_recommend(req: RecommendRequest):
    """
    AI ile akıllı öneri üretir.
    
    - Notion'dan içerikleri çeker
    - Kullanıcının ilgi alanı ve geçmişini analiz eder
    - GPT ile en uygun 5 içeriği skorlayarak döner
    """
    items = get_all_items()
    recommendations = simulate_recommendations(
        interest=req.interest,
        items=items,
        history=req.history
    )
    return {
        "interest": req.interest,
        "total_items_analyzed": len(items),
        "recommendations": recommendations
    }


@app.get("/recommend", tags=["Öneri Motoru"])
def simple_recommend(interest: str):
    """Basit öneri — sadece ilgi alanına göre (geriye uyumlu)."""
    return {
        "recommendations": get_recommendation(interest)
    }


# ──────────────────────────────────────────────
# Detaylı İnceleme (Model Seçimi)
# ──────────────────────────────────────────────

@app.post("/item-details", tags=["Öneri Motoru"])
def item_details(req: ItemDetailRequest):
    """
    Seçilen bir içeriğin detaylı model analizlerini döner.
    Kullanıcıya 3 farklı modelin açıklaması gösterilerek seçim yapması sağlanır.
    """
    details = generate_item_details(req.item_title, req.interest)
    return {
        "item_title": req.item_title,
        "details": details
    }


# ──────────────────────────────────────────────
# Feedback (Geri Bildirim 👍👎)
# ──────────────────────────────────────────────

@app.post("/feedback", tags=["Geri Bildirim"])
def submit_feedback(fb: FeedbackRequest):
    """
    Kullanıcının bir öneriye verdiği feedback'i kaydeder.
    
    Gönderilecek veri:
    {
        "user_name": "Ahmet",
        "item_title": "Python ile Makine Öğrenmesi",
        "feedback": "like"
    }
    """
    result = save_feedback(fb.user_name, fb.item_title, fb.feedback)
    return result


# ──────────────────────────────────────────────
# Zapier Webhook
# ──────────────────────────────────────────────

@app.post("/zapier-webhook", tags=["Otomasyon"])
def zapier_webhook(payload: dict):
    """
    Zapier'den gelen webhook verilerini işler.
    Beklenen format örneği: {"name": "Ahmet Yılmaz", "interest": "Yapay Zeka"}
    """
    name = payload.get("name", "Bilinmeyen Kullanıcı")
    interest = payload.get("interest", "Genel")
    
    # Not: Veri zaten Notion'dan geldiği için tekrar Notion'a EKLEMİYORUZ (Döngü olmaması için)
    # Burada AI ile öneri üretme, e-posta atma gibi işlemler yapılabilir.
    print(f"[ZAPIER WEBHOOK] Yeni veri geldi: {name} - {interest}")
    
    return {
        "status": "success",
        "message": f"{name} için Zapier verisi başarıyla alındı ve işlendi.",
        "received_data": payload
    }