"use client";

import { useState } from "react";
import { Sparkles, ShoppingBag, BookOpen, Smartphone, ThumbsUp, Eye, Star, Filter, Zap, Database } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const ALL_ITEMS = [
  { id: "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa", title: "iPhone 15 Pro", category: "electronics", icon: Smartphone, color: "text-blue-400", price: "$999", desc: "En güçlü A17 Pro çipi" },
  { id: "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb", title: "Dune - Frank Herbert", category: "books", icon: BookOpen, color: "text-orange-400", price: "$15", desc: "Ödüllü bilim kurgu başyapıtı" },
  { id: "cccccccc-cccc-cccc-cccc-cccccccccccc", title: "Sony WH-1000XM5", category: "electronics", icon: Smartphone, color: "text-indigo-400", price: "$349", desc: "Sektörün en iyi gürültü engelleme" },
  { id: "dddddddd-dddd-dddd-dddd-dddddddddddd", title: "Nike Air Max", category: "clothing", icon: ShoppingBag, color: "text-red-400", price: "$120", desc: "Klasik Air teknolojisi" },
  { id: "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee", title: "Sapiens - Yuval Noah Harari", category: "books", icon: BookOpen, color: "text-amber-400", price: "$18", desc: "İnsanlığın kısa tarihi" },
  { id: "ffffffff-ffff-ffff-ffff-ffffffffffff", title: "Samsung Galaxy S24", category: "electronics", icon: Smartphone, color: "text-cyan-400", price: "$799", desc: "Galaxy AI entegrasyonu" },
];

const CATEGORIES = ["Tümü", "electronics", "books", "clothing"];
const CATEGORY_LABELS: Record<string, string> = {
  "Tümü": "Tümü",
  electronics: "📱 Elektronik",
  books: "📚 Kitap",
  clothing: "👟 Giyim",
};

interface Rec { title: string; reason: string; score: number; }

export default function Home() {
  const [interactions, setInteractions] = useState<{ item: string; action: string; status: string }[]>([]);
  const [recommendations, setRecommendations] = useState<Rec[]>([]);
  const [recSource, setRecSource] = useState<string | null>(null);
  const [loadingAI, setLoadingAI] = useState(false);
  const [activeCategory, setActiveCategory] = useState("Tümü");

  const API_INTERACTION = "/api/interaction";
  const API_RECOMMEND   = "/api/recommend";
  const USER_ID         = "11111111-1111-1111-1111-111111111111";

  const filteredItems = activeCategory === "Tümü"
    ? ALL_ITEMS
    : ALL_ITEMS.filter(i => i.category === activeCategory);

  const handleInteraction = async (itemId: string, itemTitle: string, action: string) => {
    setInteractions(prev => [{ item: itemTitle, action, status: "gönderiliyor..." }, ...prev].slice(0, 6));
    try {
      const res = await fetch(API_INTERACTION, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: USER_ID, item_id: itemId, action }),
      });
      const status = res.ok ? "✓ n8n'e kaydedildi" : "⚠ hata";
      setInteractions(prev => [{ ...prev[0], status }, ...prev.slice(1)]);
    } catch {
      setInteractions(prev => [{ ...prev[0], status: "⚠ bağlantı hatası" }, ...prev.slice(1)]);
    }
  };

  const getRecommendations = async () => {
    setLoadingAI(true);
    setRecommendations([]);
    setRecSource(null);
    try {
      const res = await fetch(API_RECOMMEND, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: USER_ID }),
      });
      const data = await res.json();
      setRecommendations(data.recommendations ?? []);
      setRecSource(data.source ?? "n8n");
    } catch {
      setRecommendations([]);
    } finally {
      setLoadingAI(false);
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-8 max-w-7xl mx-auto flex flex-col gap-8">
      {/* Header */}
      <header className="flex flex-wrap justify-between items-center gap-4 pb-6 border-b border-[var(--border)]">
        <div>
          <h1 className="text-3xl md:text-4xl font-bold tracking-tight mb-1 flex items-center gap-3">
            <Sparkles className="text-blue-500 w-8 h-8" />
            <span className="gradient-text">AI Öneri Motoru</span>
          </h1>
          <p className="text-slate-400 text-sm">n8n Workflow Engine · PostgreSQL · Redis · Qdrant ile güçlendirildi</p>
        </div>
        <div className="flex items-center gap-2 glass-panel px-4 py-2 rounded-full text-sm font-medium">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
          n8n Aktif · localhost:5678
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Sol - Ürünler */}
        <div className="lg:col-span-2 flex flex-col gap-5">
          {/* Kategori Filtresi */}
          <div className="flex items-center gap-2 flex-wrap">
            <Filter className="w-4 h-4 text-slate-400 shrink-0" />
            {CATEGORIES.map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all ${
                  activeCategory === cat
                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-900/30"
                    : "glass-panel text-slate-400 hover:text-white"
                }`}
              >
                {CATEGORY_LABELS[cat]}
              </button>
            ))}
          </div>

          {/* Ürün Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <AnimatePresence mode="popLayout">
              {filteredItems.map((item, idx) => {
                const Icon = item.icon;
                return (
                  <motion.div
                    key={item.id}
                    layout
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.95 }}
                    transition={{ delay: idx * 0.05 }}
                    className="glass-panel p-5 rounded-2xl flex flex-col gap-4 hover:border-indigo-500/50 transition-colors"
                  >
                    <div className="flex justify-between items-start">
                      <div className={`p-3 rounded-xl bg-slate-800 ${item.color}`}>
                        <Icon className="w-5 h-5" />
                      </div>
                      <span className="font-mono text-slate-300 font-bold text-sm">{item.price}</span>
                    </div>
                    <div>
                      <h3 className="text-lg font-bold">{item.title}</h3>
                      <p className="text-xs text-slate-500 mt-0.5">{item.desc}</p>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleInteraction(item.id, item.title, "view")}
                        className="flex-1 bg-slate-800 hover:bg-slate-700 text-sm py-2 rounded-lg flex items-center justify-center gap-2 transition-colors"
                      >
                        <Eye className="w-4 h-4" /> İncele
                      </button>
                      <button
                        onClick={() => handleInteraction(item.id, item.title, "like")}
                        className="flex-1 bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 text-sm py-2 rounded-lg flex items-center justify-center gap-2 transition-colors"
                      >
                        <ThumbsUp className="w-4 h-4" /> Beğen
                      </button>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>
          </div>
        </div>

        {/* Sağ - AI Panel */}
        <div className="flex flex-col gap-6">
          {/* Öneri Paneli */}
          <div className="glass-panel p-6 rounded-2xl border border-indigo-500/30 relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-500 to-purple-500" />
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-400" />
                Sizin İçin Seçilenler
              </h2>
              {recSource && (
                <span className={`text-xs px-2 py-1 rounded-full font-mono flex items-center gap-1 ${
                  recSource === "n8n"
                    ? "bg-green-900/40 text-green-400"
                    : "bg-slate-700 text-slate-400"
                }`}>
                  {recSource === "n8n"
                    ? <><Zap className="w-3 h-3" /> n8n</>
                    : <><Database className="w-3 h-3" /> fallback</>}
                </span>
              )}
            </div>

            <button
              onClick={getRecommendations}
              disabled={loadingAI}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 py-3 rounded-xl font-medium shadow-lg shadow-blue-900/20 mb-5 transition-all disabled:opacity-50 flex justify-center items-center gap-2 text-sm"
            >
              {loadingAI
                ? <><div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> n8n AI çalışıyor...</>
                : "Yapay Zeka ile Öneri Getir"}
            </button>

            <div className="flex flex-col gap-3">
              {recommendations.length === 0 && !loadingAI && (
                <p className="text-slate-500 text-xs text-center py-3">Ürünlerle etkileşime geçin veya butona tıklayın.</p>
              )}
              <AnimatePresence>
                {recommendations.map((rec, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: idx * 0.12 }}
                    className="bg-slate-800/50 p-4 rounded-xl border border-slate-700"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-bold text-blue-300 text-sm leading-snug">{rec.title}</h4>
                      {rec.score > 0 && (
                        <span className="text-xs font-mono bg-blue-900/50 text-blue-400 px-2 py-0.5 rounded-md shrink-0 ml-2">
                          %{Math.round(rec.score * 100)}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-slate-400 leading-relaxed">{rec.reason}</p>
                  </motion.div>
                ))}
              </AnimatePresence>
            </div>
          </div>

          {/* Canlı Log */}
          <div className="glass-panel p-5 rounded-2xl">
            <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3 flex items-center gap-2">
              <Star className="w-4 h-4" />
              n8n Canlı Etkileşim Logu
            </h2>
            <div className="flex flex-col gap-2 max-h-52 overflow-y-auto">
              {interactions.length === 0
                ? <p className="text-xs text-slate-600">Henüz etkileşim yok. Ürünlere tıklayın!</p>
                : interactions.map((interaction, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: -8 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="text-xs p-3 rounded-lg bg-slate-900/60 border-l-2 border-indigo-500"
                    >
                      <div>
                        <span className="text-blue-400 font-semibold">{interaction.item}</span>
                        {" "}
                        <span className="text-emerald-400">{interaction.action === "like" ? "beğenildi" : "incelendi"}</span>
                      </div>
                      <span className="text-slate-600 font-mono">{interaction.status}</span>
                    </motion.div>
                  ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
