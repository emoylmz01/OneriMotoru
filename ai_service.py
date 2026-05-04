"""
AI Öneri Servisi — OpenAI GPT ile akıllı öneri üretimi.
"""
import json
import random
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_recommendation(interest: str):
    """
    Basit öneri — sadece ilgi alanına göre 3 öneri üretir.
    (Eski endpoint için geriye uyumlu)
    """
    prompt = f"""
    Kullanıcının ilgi alanı: {interest}
    
    Buna göre 3 tane öneri yap.
    Kısa ve net olsun.
    """

    # Simulated fallback recommendations (no external API call)
    fallback = [
        f"{interest} ile ilgili öneri 1",
        f"{interest} ile ilgili öneri 2",
        f"{interest} ile ilgili öneri 3"
    ]
    return "\n".join(fallback)


def generate_smart_recommendations(interest: str, items: list, history: list = None):
    """
    Gelişmiş öneri motoru (Çoklu Model Simülasyonu):
    Kullanıcının ilgi alanına göre 3 farklı yapay zeka modelini (OpenAI, Gemini, Claude)
    simüle ederek karşılaştırmalı sonuçlar döner.
    """
    # 3 farklı model için simülasyon sonuçlarını oluştur
    openai_results = _simulate_model(interest, items, "openai")
    gemini_results = _simulate_model(interest, items, "gemini")
    claude_results = _simulate_model(interest, items, "claude")

    return {
        "OpenAI": openai_results,
        "Gemini": gemini_results,
        "Claude": claude_results
    }

def simulate_recommendations(interest: str, items: list, history: list = None):
    """Public wrapper that returns simulated recommendations for OpenAI, Gemini and Claude.
    Internally reuses generate_smart_recommendations which already creates model‑specific results.
    """
    return generate_smart_recommendations(interest, items, history)


def generate_item_details(item_title: str, interest: str = ""):
    """
    Seçilen içerik için 3 farklı modelin (OpenAI, Gemini, Claude) 
    o içeriği nasıl yorumladığını ve bir devam linkini simüle eder.
    """
    
    # Simüle edilmiş linkler
    search_query = item_title.replace(" ", "+")
    
    return {
        "OpenAI": {
            "text": f"OpenAI Analizi: '{item_title}' içeriği, özellikle '{interest}' alanındaki teknik temelleri güçlendirmek için ideal bir kaynaktır. İçeriğin yapısal yaklaşımı, algoritmaların veya sistemlerin nasıl çalıştığını adım adım anlamanızı sağlar. Standart yöntemler ve en iyi uygulamalar üzerinden ilerleyerek teorik bilginizi pratikle birleştirmenize olanak tanır.",
            "link": f"https://platform.openai.com/docs/search?q={search_query}"
        },
        "Gemini": {
            "text": f"Gemini Analizi: '{item_title}' konusunu geniş bir ekosistem perspektifinden değerlendirmek gerekirse, '{interest}' vizyonunuza büyük bir hız kazandıracaktır. Google'ın geniş veri ağından beslenen trendlere baktığımızda, bu konunun gelecekteki projelerde çok daha entegre bir rol oynayacağını söyleyebiliriz. Hızlı büyüme ve geniş çaplı uygulanabilirlik açısından mükemmel bir başlangıç.",
            "link": f"https://gemini.google.com/search?q={search_query}"
        },
        "Claude": {
            "text": f"Claude Analizi: '{item_title}' içeriği bana kalırsa sadece teknik bir öğrenme değil, aynı zamanda '{interest}' hedeflerinize ulaşırken insani odaklı ve güvenli sistemler tasarlamanız için harika bir rehber. Etik boyutları, güvenlik adımlarını ve kullanıcı odaklı mimariyi merkeze alarak, bu konuyu derinlemesine ve sorumlu bir şekilde öğrenmeniz için en uygun araçtır.",
            "link": f"https://claude.ai/search?q={search_query}"
        }
    }


def _simulate_model(interest: str, items: list, model_type: str):
    """
    Farklı modellerin karakteristiğini taklit eden öneri algoritması.
    """
    interest_words = set(interest.lower().split())
    scored = []

    for item in items:
        tags = set(t.lower() for t in item.get("tags", []))
        category = item.get("category", "").lower()
        title = item.get("title", "").lower()

        # Temel eşleşmeler
        overlap = len(interest_words & tags)
        cat_match = 1 if any(w in category for w in interest_words) else 0
        title_match = 1 if any(w in title for w in interest_words) else 0

        # Model karakteristikleri (Farklı ağırlıklandırmalar)
        if model_type == "openai":
            # OpenAI: Dengeli ve etiket odaklı
            raw_score = (overlap * 35) + (cat_match * 20) + (title_match * 20) + random.randint(5, 10)
            reason = "İlgi alanınızla etiket/kategori eşleşmesi bulundu."
        elif model_type == "gemini":
            # Gemini: Kategori ve geniş bağlam odaklı
            raw_score = (overlap * 20) + (cat_match * 40) + (title_match * 15) + random.randint(10, 20)
            reason = "Kategorisel bağlamda aramanızla yüksek alaka tespit edildi."
        else: # claude
            # Claude: Başlık ve spesifik eşleşme odaklı
            raw_score = (overlap * 15) + (cat_match * 15) + (title_match * 50) + random.randint(0, 5)
            reason = "İçerik başlığı doğrudan aradığınız konuyla örtüşüyor."

        score = min(100, max(0, raw_score))

        # Yalnızca biraz da olsa alakası olanları veya rastgele birkaçını ekle
        if score > 15 or len(items) <= 5:
            scored.append({
                "title": item["title"],
                "score": score,
                "reason": reason
            })

    # Skora göre sırala ve en iyi 5'i al
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:5]