-- ==============================================
-- 🔰 SEED DATA HOTEL MAJU JAYA (Versi Lengkap)
-- ==============================================

-- =====================
-- TABEL: KAMAR
-- =====================
DELETE FROM api_hotel_kamar;

INSERT INTO api_hotel_kamar (
    nomor_kamar, tipe_kamar, harga_per_malam, kapasitas, fasilitas,
    diskon_persen, catatan_diskon, url_gambar
) VALUES
('101', 'Standard', 450000.00, 2, 'AC, TV, Kamar mandi dalam, Wi-Fi gratis', 0, NULL, 'https://example.com/images/standard1.jpg'),
('102', 'Standard', 450000.00, 2, 'AC, TV, Kamar mandi dalam, Wi-Fi gratis', 10, 'Promo Awal Minggu', 'https://example.com/images/standard2.jpg'),
('103', 'Superior', 550000.00, 2, 'AC, TV, Air panas, Balkon kecil, Wi-Fi gratis', 5, 'Diskon Member', 'https://example.com/images/superior1.jpg'),
('201', 'Deluxe', 650000.00, 3, 'AC, TV, Air panas, Balkon, Wi-Fi gratis, Sarapan', 15, 'Diskon Akhir Pekan', 'https://example.com/images/deluxe1.jpg'),
('202', 'Deluxe', 650000.00, 3, 'AC, TV, Air panas, Balkon, Wi-Fi gratis, Sarapan', 0, NULL, 'https://example.com/images/deluxe2.jpg'),
('301', 'Suite', 950000.00, 4, 'AC, TV, Bathtub, Balkon, Ruang tamu, Wi-Fi, Sarapan', 20, 'Promo Musim Liburan', 'https://example.com/images/suite1.jpg'),
('302', 'Suite', 950000.00, 4, 'AC, TV, Bathtub, Balkon, Ruang tamu, Wi-Fi, Sarapan', 0, NULL, 'https://example.com/images/suite2.jpg'),
('401', 'Family Suite', 1250000.00, 5, '2 Kamar tidur, Ruang tamu, Dapur kecil, Balkon, Wi-Fi', 10, 'Diskon Liburan Keluarga', 'https://example.com/images/family.jpg'),
('501', 'Presidential Suite', 3500000.00, 6, '3 Kamar tidur, Jacuzzi, Ruang tamu luas, Private bar, Balkon besar', 25, 'VIP Promo', 'https://example.com/images/presidential.jpg');

-- =====================
-- TABEL: FAQ
-- =====================
DELETE FROM api_hotel_faq;

INSERT INTO api_hotel_faq (pertanyaan, jawaban, kategori) VALUES
('Jam check-in dan check-out?', 'Check-in mulai pukul 14:00 WIB, dan check-out maksimal pukul 12:00 WIB.', 'reservasi'),
('Apakah sarapan sudah termasuk?', 'Ya, semua harga kamar sudah termasuk sarapan untuk dua orang.', 'fasilitas'),
('Apakah tersedia Wi-Fi gratis?', 'Ya, Wi-Fi gratis tersedia di seluruh area hotel.', 'fasilitas'),
('Bagaimana cara membatalkan reservasi?', 'Pembatalan dapat dilakukan maksimal 24 jam sebelum check-in tanpa biaya.', 'reservasi'),
('Apakah tersedia layanan antar-jemput bandara?', 'Ya, tersedia dengan biaya tambahan. Silakan hubungi resepsionis.', 'layanan'),
('Apakah hotel menerima pembayaran QRIS?', 'Ya, kami menerima QRIS, kartu debit, dan transfer bank.', 'pembayaran'),
('Apakah anak-anak boleh menginap?', 'Tentu, anak-anak boleh menginap gratis jika berbagi tempat tidur dengan orang tua.', 'kebijakan'),
('Apakah ada kamar bebas rokok?', 'Ya, beberapa kamar kami adalah bebas rokok. Mohon informasikan saat reservasi.', 'kebijakan'),
('Apakah tersedia ruang meeting?', 'Ya, kami memiliki ruang meeting berkapasitas hingga 50 orang.', 'fasilitas'),
('Apakah bisa late check-out?', 'Bisa hingga pukul 15:00 jika kamar tersedia, dengan tambahan 50% dari tarif kamar.', 'reservasi'),
('Apakah hotel menyediakan layanan laundry?', 'Ya, layanan laundry tersedia setiap hari pukul 08:00–20:00 WIB.', 'layanan'),
('Apakah hotel menyediakan layanan kebersihan kamar setiap hari?', 'Ya, housekeeping beroperasi setiap hari dari pukul 08:00–16:00 WIB.', 'layanan'),
('Apakah hewan peliharaan diperbolehkan?', 'Mohon maaf, hotel kami tidak mengizinkan hewan peliharaan.', 'kebijakan'),
('Apakah hotel memiliki area musholla?', 'Ya, tersedia musholla di lantai dasar dekat lobby.', 'fasilitas'),
('Apakah ada minimarket di sekitar hotel?', 'Ada, minimarket tersedia di area parkir depan hotel.', 'lokasi'),
('Apakah ada layanan pijat/spa?', 'Ya, tersedia layanan Spa & Massage profesional di lantai 2.', 'layanan'),
('Berapa harga sarapan tambahan?', 'Sarapan tambahan dikenakan biaya Rp50.000 per orang.', 'pembayaran'),
('Apakah tersedia parkir gratis?', 'Ya, parkir gratis untuk semua tamu hotel.', 'fasilitas'),
('Apakah hotel menyediakan layanan sewa mobil?', 'Ya, kami menyediakan layanan sewa mobil dan tour guide.', 'layanan'),
('Apakah hotel menerima reservasi grup?', 'Ya, kami melayani reservasi untuk rombongan atau acara besar.', 'reservasi');

-- =====================
-- TABEL: FASILITAS UMUM
-- =====================
DELETE FROM api_hotel_fasilitasumum;

INSERT INTO api_hotel_fasilitasumum (
    nama_fasilitas, deskripsi, jam_buka, lokasi, gambar_url
) VALUES
('Kolam Renang', 'Kolam renang outdoor dengan pemandangan taman dan kursi santai.', '07:00 - 18:00 WIB', 'Lantai 1 - Area Belakang', 'https://example.com/images/kolam.jpg'),
('Restoran Maju Jaya', 'Menyajikan masakan lokal dan internasional, tersedia sarapan buffet.', '06:00 - 22:00 WIB', 'Lantai Dasar', 'https://example.com/images/restoran.jpg'),
('Gym & Fitness Center', 'Dilengkapi alat modern dan pelatih profesional.', '06:00 - 22:00 WIB', 'Lantai 2', 'https://example.com/images/gym.jpg'),
('Ruang Meeting', 'Ruang rapat modern dengan proyektor, Wi-Fi, dan sound system.', '08:00 - 20:00 WIB', 'Lantai 3', 'https://example.com/images/meetingroom.jpg'),
('Spa & Massage', 'Layanan pijat dan relaksasi dengan terapis berpengalaman.', '09:00 - 21:00 WIB', 'Lantai 2', 'https://example.com/images/spa.jpg'),
('Area Parkir', 'Area parkir luas dan gratis untuk tamu hotel.', '24 Jam', 'Depan Hotel', 'https://example.com/images/parkir.jpg'),
('Musholla', 'Tempat ibadah yang bersih dan tenang untuk tamu muslim.', '24 Jam', 'Dekat Lobby Utama', 'https://example.com/images/musholla.jpg'),
('Playground Anak', 'Area bermain anak dengan perosotan dan ayunan aman.', '07:00 - 18:00 WIB', 'Samping Kolam Renang', 'https://example.com/images/playground.jpg'),
('Rooftop Bar', 'Bar di rooftop dengan pemandangan kota dan live music setiap malam.', '17:00 - 00:00 WIB', 'Lantai Atas', 'https://example.com/images/rooftop.jpg'),
('Charging Station', 'Tersedia area charging untuk mobil listrik.', '24 Jam', 'Area Parkir', 'https://example.com/images/charging.jpg');

-- =====================
-- TABEL: PELAYANAN
-- =====================
DELETE FROM api_hotel_pelayanan;

INSERT INTO api_hotel_pelayanan (nama_layanan, deskripsi, biaya, jam_operasional, gambar_url) VALUES
('Layanan Laundry', 'Cuci dan setrika pakaian tamu hotel.', 25000.00, '08:00 - 20:00 WIB', 'https://example.com/images/laundry.jpg'),
('Spa & Massage', 'Paket pijat relaksasi dengan terapis profesional.', 100000.00, '09:00 - 21:00 WIB', 'https://example.com/images/spa.jpg'),
('Antar-Jemput Bandara', 'Transportasi dari/ke bandara dengan mobil hotel.', 150000.00, '24 Jam', 'https://example.com/images/shuttle.jpg'),
('Room Service', 'Pesan makanan/minuman langsung dari kamar.', 30000.00, '06:00 - 23:00 WIB', 'https://example.com/images/roomservice.jpg'),
('Breakfast Buffet', 'Sarapan buffet di Restoran Maju Jaya.', 50000.00, '06:00 - 10:00 WIB', 'https://example.com/images/breakfast.jpg'),
('Tour Guide', 'Layanan pemandu wisata untuk tamu hotel.', 200000.00, '07:00 - 19:00 WIB', 'https://example.com/images/tourguide.jpg'),
('Valet Parking', 'Petugas parkir profesional yang siap membantu.', 0.00, '24 Jam', 'https://example.com/images/valet.jpg'),
('Rental Mobil', 'Sewa mobil harian dengan sopir berpengalaman.', 400000.00, '24 Jam', 'https://example.com/images/rental.jpg'),
('Candlelight Dinner', 'Makan malam romantis di rooftop dengan dekorasi spesial.', 750000.00, '18:00 - 22:00 WIB', 'https://example.com/images/dinner.jpg'),
('Mini Bar', 'Layanan mini bar untuk tamu Suite dan Family Room.', 100000.00, '24 Jam', 'https://example.com/images/minibar.jpg');
