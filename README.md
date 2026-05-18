# AI Öneri Motoru 🤖

**n8n + PostgreSQL + Redis + Qdrant** ile güçlendirilmiş gerçek zamanlı, kişiselleştirilmiş AI öneri sistemi.

## 🏗️ Mimari

```
┌─────────────────────┐
│   Next.js Frontend  │  ← http://localhost:3000
│   (React + Tailwind)│
└──────────┬──────────┘
           │ API Proxy (CORS-free)
           ▼
┌─────────────────────┐
│   n8n Workflow      │  ← http://localhost:5678
│   Engine            │
│  ┌──────────────┐   │
│  │ Webhook      │   │
│  │ AI Agent     │   │
│  │ DB İşlemleri │   │
│  └──────────────┘   │
└──────────┬──────────┘
           ▼
┌─────────────────────────────────────────┐
│           Veritabanı Katmanı            │
│  PostgreSQL  │  Redis  │  Qdrant        │
│  (Ana DB)    │  (Cache)│  (Vektör DB)   │
└─────────────────────────────────────────┘
```

## 🚀 Hızlı Başlangıç

### 1. Gereksinimleri Kur
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js 18+](https://nodejs.org/)

### 2. Altyapıyı Başlat (Docker)
```bash
# Proje kök dizininde
docker compose up -d
```

Bu komut şu servisleri başlatır:
| Servis | Port | Açıklama |
|--------|------|----------|
| n8n | 5678 | Workflow otomasyonu |
| PostgreSQL | 5432 | Ana veritabanı |
| Redis | 6379 | Önbellek |
| Qdrant | 6333 | Vektör veritabanı |

### 3. n8n'i Yapılandır
1. `http://localhost:5678` adresine git
2. Kullanıcı adı: `admin`, Şifre: `password`
3. Workflows menüsünden iş akışlarını içe aktar veya rehberi takip et

### 4. Frontend'i Başlat
```bash
cd frontend
npm install
npm run dev
```

Web arayüzü `http://localhost:3000` adresinde açılır.

## 📋 n8n Workflow'ları

### Workflow 1: Kullanıcı Etkileşim Kaydı
- **Endpoint:** `POST /webhook/interaction`
- Kullanıcı beğenme/inceleme verilerini PostgreSQL'e kaydeder
- Redis önbelleğini günceller

### Workflow 2: AI Öneri Üretici
- **Endpoint:** `POST /webhook/recommend`
- Kullanıcı geçmişine göre kişiselleştirilmiş öneriler üretir
- Yanıt formatı: `{ recommendations: [{title, reason, score}] }`

### Workflow 3: Toplu Günceleme
- Her gece otomatik çalışır (Cron)
- Tüm kullanıcılar için önerileri günceller

## 🗄️ Veritabanı Şeması

```sql
users         -- Kullanıcı profilleri
items         -- Öneri öğeleri (ürünler, içerikler)
interactions  -- Beğenme, tıklama, satın alma kayıtları
recommendations -- AI tarafından oluşturulan öneri geçmişi
```

## 🔑 Ortam Değişkenleri

`.env.example` dosyasını kopyalayın:
```bash
cp .env.example .env
```

## 🔒 Güvenlik Notu
`.env` dosyasını asla GitHub'a yüklemeyin. `.gitignore` zaten bu dosyayı dışlayacak şekilde yapılandırılmıştır.
