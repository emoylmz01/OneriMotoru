-- Vektör eklentisini (pgvector) kur (bu özellik Qdrant kullanacağımız için şart olmasa da PostgreSQL'de tutmak istersen faydalıdır)
-- Ancak standart postgres:15 imajında pgvector bulunmaz, bu yüzden bu adımı şimdilik yorum satırı yapıyoruz. Qdrant ana vektör depomuz olacak.
-- CREATE EXTENSION IF NOT EXISTS vector;

-- Kullanıcılar
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    preferences JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Ürünler/İçerikler (önerilecek öğeler)
CREATE TABLE IF NOT EXISTS items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    tags TEXT[],
    -- embedding VECTOR(1536), -- pgvector olmadığı için iptal, Qdrant'ta tutulacak
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Kullanıcı Etkileşimleri (beğenme, tıklama, satın alma)
CREATE TABLE IF NOT EXISTS interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    item_id UUID REFERENCES items(id),
    interaction_type VARCHAR(50), -- 'view', 'like', 'purchase', 'rating'
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    timestamp TIMESTAMP DEFAULT NOW()
);

-- AI Öneri Geçmişi
CREATE TABLE IF NOT EXISTS recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    item_id UUID REFERENCES items(id),
    ai_score FLOAT,
    reason TEXT, -- AI'nin önerme nedeni
    clicked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Performans İndeksleri
CREATE INDEX IF NOT EXISTS idx_interactions_user ON interactions(user_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_interactions_item ON interactions(item_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_user ON recommendations(user_id, created_at DESC);

-- Örnek Veri Ekleme (Test amaçlı)
INSERT INTO users (id, email, preferences) VALUES 
('11111111-1111-1111-1111-111111111111', 'testuser1@example.com', '{"favorite_categories": ["electronics", "books"]}'),
('22222222-2222-2222-2222-222222222222', 'testuser2@example.com', '{"favorite_categories": ["clothing"]}');

INSERT INTO items (id, title, description, category, tags) VALUES 
('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Akıllı Telefon', 'Yeni nesil yüksek performanslı akıllı telefon', 'electronics', '{"tech", "mobile"}'),
('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Bilim Kurgu Romanı', 'Derin uzay macerası anlatan ödüllü roman', 'books', '{"fiction", "space"}'),
('cccccccc-cccc-cccc-cccc-cccccccccccc', 'Erkek T-Shirt', 'Pamuklu rahat günlük t-shirt', 'clothing', '{"casual", "summer"}');
