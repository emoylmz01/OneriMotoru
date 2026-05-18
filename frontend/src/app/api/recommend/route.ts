import { NextRequest, NextResponse } from "next/server";

const N8N_RECOMMEND_URL = "http://localhost:5678/webhook/recommend";

// n8n'den gelen herhangi bir yapıyı normalize et
function normalizeRecommendations(data: unknown): Array<{title: string; reason: string; score: number}> {
  // Dizi ise direkt kullan
  if (Array.isArray(data)) {
    return data
      .map((item: unknown) => {
        const d = item as Record<string, unknown>;
        // n8n Code node bazen {json: {...}} formatında döner
        const actual = (d?.json ?? d) as Record<string, unknown>;
        if (actual?.recommendations && Array.isArray(actual.recommendations)) {
          return actual.recommendations as Array<{title: string; reason: string; score: number}>;
        }
        return actual as {title: string; reason: string; score: number};
      })
      .flat()
      .filter((r: unknown) => {
        const rec = r as Record<string, unknown>;
        return rec?.title || rec?.reason;
      })
      .map((r: unknown) => {
        const rec = r as Record<string, unknown>;
        return {
          title: String(rec.title || "Öneri"),
          reason: String(rec.reason || rec.explanation || rec.description || "Geçmiş etkileşimlerinize göre önerildi."),
          score: Number(rec.score ?? rec.confidence ?? 0.8),
        };
      });
  }
  
  // Obje ise recommendations anahtarını ara
  if (data && typeof data === "object") {
    const obj = data as Record<string, unknown>;
    const inner = obj?.recommendations ?? obj?.data ?? obj?.items ?? obj?.result;
    if (Array.isArray(inner)) return normalizeRecommendations(inner);
    // Tek öneri objesi ise diziye çevir
    if (obj?.title) {
      return [{
        title: String(obj.title),
        reason: String(obj.reason ?? obj.explanation ?? "Kişisel tercihlerinize göre seçildi."),
        score: Number(obj.score ?? 0.8),
      }];
    }
  }
  
  return [];
}

// Kullanıcı etkileşimlerine göre zengin Türkçe öneriler (fallback)
const FALLBACK_RECS = [
  {
    title: "Samsung Galaxy S24 Ultra",
    reason: "iPhone 15 Pro'ya ilgi gösterdiniz — Samsung, benzer amiral gemisi özelliklerini Android ekosistemiyle sunar ve kamera kalitesiyle öne çıkar.",
    score: 0.95,
  },
  {
    title: "Sony WF-1000XM5 Kablosuz Kulaklık",
    reason: "Sony WH-1000XM5'i incelediğiniz için aynı serideki kompakt kablosuz modeli önerdik; aktif gürültü engelleme teknolojisi eşsiz.",
    score: 0.91,
  },
  {
    title: "Sapiens: İnsan Türünün Kısa Tarihi",
    reason: "Dune gibi geniş ufuklu eserleri beğeniyorsunuz — Sapiens, insanlık tarihini aynı derinlik ve akıcılıkla ele alan bir başyapıt.",
    score: 0.88,
  },
  {
    title: "Apple AirPods Pro 2",
    reason: "Apple iPhone 15 Pro'yu incelemeniz ekosistem tercihinizi ortaya koyuyor; AirPods Pro ile mükemmel entegrasyon sağlarsınız.",
    score: 0.87,
  },
  {
    title: "Adidas Ultraboost 23",
    reason: "Nike Air Max'e olan ilginiz spor ayakkabısı kategorisinde aktif olduğunuzu gösteriyor — Ultraboost koşu performansıyla rakipsiz.",
    score: 0.82,
  },
];

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const n8nRes = await fetch(N8N_RECOMMEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const text = await n8nRes.text();
    let data: unknown;
    try { data = JSON.parse(text); } catch { data = null; }

    // n8n yanıtını normalize et
    const recommendations = normalizeRecommendations(data);

    // n8n anlamlı veri döndüremediyse fallback kullan
    const finalRecs = recommendations.length > 0 ? recommendations : FALLBACK_RECS;

    return NextResponse.json({ recommendations: finalRecs, source: recommendations.length > 0 ? "n8n" : "fallback" });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Bilinmeyen hata";
    console.error("n8n öneri hatası:", message);
    // Hata durumunda da zengin fallback döndür
    return NextResponse.json({ recommendations: FALLBACK_RECS, source: "fallback-error" });
  }
}
