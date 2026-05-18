import { NextRequest, NextResponse } from "next/server";

const N8N_INTERACTION_URL = "http://localhost:5678/webhook/interaction";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const n8nRes = await fetch(N8N_INTERACTION_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const text = await n8nRes.text();
    let data: unknown;
    try { data = JSON.parse(text); } catch { data = { raw: text }; }

    return NextResponse.json({ status: "ok", n8n: data }, { status: n8nRes.status });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Bilinmeyen hata";
    return NextResponse.json(
      { status: "error", message: `n8n bağlantı hatası: ${message}` },
      { status: 502 }
    );
  }
}
