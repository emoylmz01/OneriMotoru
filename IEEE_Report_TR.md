# Zapier Entegrasyonu ile Otomatize Edilmiş Çoklu Modelli Yapay Zeka Öneri Mimarisi

**Özet**— Bu çalışma, olay tabanlı (event-driven) bir yapay zeka öneri sisteminin mimarisini ve pratik uygulamasını detaylandırmaktadır. Sistem, yapılandırılmış verilere dayanarak içerik değerlendirmesi yapmak ve öneriler sunmak üzere birden fazla Büyük Dil Modelini (LLM) entegre etmektedir. FastAPI, bir Notion veritabanı ile üç bağımsız yapay zeka sağlayıcısı (OpenAI, Gemini ve Claude) arasındaki etkileşimleri koordine eden temel arka uç (backend) yönlendirme katmanı olarak görev yapmaktadır. Veri akışını otomatize etmek ve manuel senkronizasyon ihtiyacını ortadan kaldırmak amacıyla ara katman (middleware) olarak Zapier kullanılmıştır. Bu entegrasyon, yeni veri girişleri tespit edildiğinde tetikleyici tabanlı ve gerçek zamanlı önerilerin üretilmesine olanak tanır. Ortaya çıkan mimari, farklı LLM çıktılarının üretim ortamında yan yana karşılaştırılması için yüksek derecede modüler bir altyapı sağlamaktadır.

**Anahtar Kelimeler**— Öneri Sistemleri, Büyük Dil Modelleri, İş Akışı Otomasyonu, API Entegrasyonu, FastAPI.

### I. GİRİŞ

Yapay zekanın içerik yönetim sistemlerine entegrasyonu, kararlı veri akışları ve düşük gecikmeli işleme gerektirir. Geleneksel öneri motorları genellikle periyodik toplu işleme (batch processing) yöntemlerine dayanır, bu da gecikmeli çıktılara ve güncelliğini yitirmiş önerilere yol açabilir. Olay tabanlı mimariler, veri durumundaki değişikliklerin hemen ardından hesaplama görevlerini tetikleyerek bu sorunu hafifletir.

Bu proje, merkezi bir çalışma alanına (Notion) bağlı, çok modelli bir yapay zeka öneri motorunun dağıtımını incelemektedir. Temel hedef, kullanıcı girişlerinin veya yeni veritabanı kayıtlarının anında kişiselleştirilmiş öneriler ürettiği kesintisiz ve otomatik bir iş akışı oluşturmaktır. Sistem, OpenAI, Gemini ve Claude modellerini eşzamanlı olarak çalıştırarak, model doğruluğu ve yanıt gecikmesi açısından bir karşılaştırma analizi aracı olarak da işlev görmektedir.

### II. SİSTEM MİMARİSİ

Sistem tasarımı, veri depolama, iş mantığı, otomasyon ve sunum katmanlarını birbirinden ayıran mikroservis odaklı bir yaklaşım izlemektedir.

**A. Veri Katmanı (Notion)**
Notion, birincil İçerik Yönetim Sistemi (CMS) olarak işlev görür. Kullanıcı profillerini, geçmiş tercihleri ve ürün/içerik kataloğunu depolar. Notion veritabanlarının yapılandırılmış doğası, veriler yapay zeka modellerine iletilmeden önce hassas sorgulamaya ve şema doğrulamasına olanak tanır.

**B. Otomasyon Ara Katmanı (Zapier)**
Zapier, olay dinleyicisi ve webhook dağıtıcısı olarak görev yapar. İş akışı (Zap) aşağıdaki gibi yapılandırılmıştır:
1. **Tetikleyici (Trigger):** Belirlenen Notion veritabanına yeni bir satır eklenir veya mevcut satır güncellenir.
2. **Aksiyon 1:** Zapier, kaydın meta verilerini çıkarır ve standart bir JSON yükü (payload) formatına dönüştürür.
3. **Aksiyon 2:** FastAPI arka uç uç noktasına (`/api/recommend/zapier-webhook`) bir POST isteği gönderilir.
4. **Aksiyon 3 (Opsiyonel):** İşlenmiş öneri arka uçtan alındığında, Zapier çıktıyı belirli bir Notion sütununa geri yazar veya belirlenen bir kanal (örn. Slack veya E-posta) üzerinden bildirim gönderir.

**C. Uygulama Katmanı (FastAPI)**
Arka uç, asenkron işlemlere yönelik yerel desteği nedeniyle FastAPI ile geliştirilmiştir. Zapier'den gelen webhook alındığında, API yükü Pydantic modelleri kullanarak doğrular. Ardından, ilgili LLM API'lerine yönelik istekleri paralelleştirir. API hız sınırına (rate limit) ulaşılması durumunda, sistem yedek (fallback) mekanizması olarak etiket eşleştirme tabanlı sezgisel bir algoritmaya geçer.

**D. Yapay Zeka Orkestrasyonu**
Motor, formatlanmış istemleri (prompt) üç farklı uç noktaya yönlendirir:
- OpenAI API (GPT-4 / 3.5)
- Google Gemini API
- Anthropic Claude API
Yanıtlar, ön yüz (frontend) istemcisinin kullanıcı değerlendirmesi için sonuçları yan yana görüntülemesini sağlayacak standart bir veri yapısında birleştirilir.

### III. UYGULAMA DETAYLARI

Uygulama, LLM sağlayıcılarına yapılan API çağrıları sırasında I/O blokajını önlemek için yoğun bir şekilde asenkron istek yönetimine dayanmaktadır.

Zapier yapılandırmasında, özel başlık (header) kimlik doğrulaması ve ham JSON iletimini sağlamak için standart uygulama modülleri yerine "Webhook by Zapier" modülü kullanılmıştır. FastAPI sunucusu, geliştirme ve dağıtım aşamaları arasında ortam tutarlılığını korumak için Docker (`Dockerfile` ve `docker-compose.yml`) kullanılarak konteynerize edilmiştir.

Kritik bir uygulama detayı da yedekleme (fallback) mantığıdır. Harici API gecikmelerini veya kota aşımlarını yönetmek için, ürün etiketlerini ve kullanıcı tercih vektörlerini işleyen yerel bir kosinüs benzerliği (cosine similarity) fonksiyonu devreye girer. Bu durum, Zapier iş akışının harici sağlayıcı kesintileri nedeniyle asla başarısız olmamasını garanti eder.

### IV. SONUÇLAR VE DEĞERLENDİRME

İlk testler, Zapier entegrasyonunun veri girişi ile önerinin hazır olması arasındaki süreyi ortalama 3.2 saniyeye düşürdüğünü göstermektedir. LLM isteklerinin FastAPI içerisinde paralel olarak yürütülmesi, genel sistem gecikmesinin tüm sağlayıcıların gecikmelerinin toplamı yerine, sadece en yavaş yapay zeka sağlayıcısının gecikmesiyle sınırlı kalmasını sağlar.

Modüler tasarım, temel Zapier otomasyon döngüsünü yeniden yapılandırmadan yeni yapay zeka modellerinin hızlı bir şekilde eklenmesine olanak tanır. Ayrıca, standardize edilmiş çıktı formatı, ön yüz uygulamalarının (Bootstrap ile geliştirilen) karşılaştırmalı görünümleri sorunsuz bir şekilde oluşturmasını sağlar.

### V. SONUÇ

Bu proje, oldukça verimli ve olay tabanlı bir öneri mimarisini ortaya koymaktadır. Veri hattı otomasyonu Zapier'e devredilerek, geliştirme kaynakları çok modelli yapay zeka mantığını ve arka uç performansını optimize etmeye odaklanmıştır. Ortaya çıkan sistem ölçeklenebilir olup, yerel yedekleme mekanizmaları sayesinde hata toleransına sahiptir ve farklı Büyük Dil Modellerini gerçek zamanlı içerik önerisi senaryolarında değerlendirmek için sağlam bir platform sunar.

### REFERANSLAR
[1] A. Vaswani et al., "Attention is all you need," Advances in neural information processing systems, 2017.
[2] S. Ramírez-Gallego et al., "Data processing and workflow automation in modern web architectures," IEEE Access, 2020.
[3] FastAPI Documentation. [Çevrimiçi]. Erişim: https://fastapi.tiangolo.com/
[4] Zapier Platform Guidelines. [Çevrimiçi]. Erişim: https://platform.zapier.com/
