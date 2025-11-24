# api_hotel/rag_router.py
# File ini berisi semua logika RAG (Retrieval-Augmented Generation)
# agar bisa modular dan mudah dimodifikasi.

import json
from django.utils import timezone
from .models import Kamar, FAQ, FasilitasUmum, Pelayanan, HotelInfo, Reservasi
from .serializers import (
    KamarSerializer, FAQSerializer, FasilitasUmumSerializer, 
    PelayananSerializer, HotelInfoSerializer, ReservasiSerializer
)
# Impor template dari file baru kita
from .prompt_template import PROMPT_TEMPLATE

def get_intents_from_message(user_message):
    """
    Fungsi RAG - Retriever (Pengambil) sederhana.
    Ini menggunakan logika 'elif' (if) untuk mendeteksi kata kunci
    dan menentukan data apa yang perlu diambil.
    """
    intents = set()
    msg_lower = user_message.lower()

    # Kategori ini bisa Anda samakan dengan 'kategori' di model FAQ Anda
    # (misal: 'kamar', 'fasilitas', 'layanan', 'reservasi', 'kebijakan')
    
    if any(k in msg_lower for k in ['kamar', 'harga', 'suite', 'deluxe', 'standard', 'menginap']):
        intents.add('KAMAR')
    if any(k in msg_lower for k in ['fasilitas', 'kolam', 'gym', 'restoran', 'meeting']):
        intents.add('FASILITAS')
    if any(k in msg_lower for k in ['layanan', 'spa', 'laundry', 'antar-jemput', 'sewa mobil']):
        intents.add('PELAYANAN')
    if any(k in msg_lower for k in ['check-in', 'check-out', 'wifi', 'parkir', 'sarapan', 'qris', 'jam berapa', 'kebijakan']):
        intents.add('FAQ')
    if any(k in msg_lower for k in ['reservasi', 'booking', 'pesan', 'ketersediaan']):
        intents.add('RESERVASI')
        
    # Fallback: Jika tidak ada intent, anggap sebagai pertanyaan umum (FAQ)
    if not intents:
        intents.add('FAQ')
        
    return intents

# ... (import dan get_intents_from_message tetap sama) ...

def retrieve_context_data(intents):
    """
    Fungsi RAG - Retrieval (Pengambilan).
    """
    context_data = {}
    placeholder = "[DATA TIDAK DIAMBIL KARENA TIDAK RELEVAN]"

    # === PASTIKAN 5 BARIS INI LENGKAP ===
    context_data['DATA_KAMAR_JSON'] = placeholder
    context_data['DATA_RESERVASI_JSON'] = "[AI TIDAK MEMILIKI AKSES KE DATA INI]"
    context_data['DATA_FASILITAS_JSON'] = placeholder
    context_data['DATA_PELAYANAN_JSON'] = placeholder  # <-- INI YANG MUNGKIN HILANG
    context_data['DATA_FAQ_JSON'] = placeholder
    # ========================================
    
    # Ambil Info Hotel & No WA (Wajib)
    hotel_info_obj = HotelInfo.objects.first()
    info_data = HotelInfoSerializer(hotel_info_obj).data if hotel_info_obj else {}
    
    context_data['NOMOR_WA_DISPLAY'] = "Nomor WhatsApp tidak tersedia"
    context_data['NOMOR_WA_URL'] = "" 
    if hotel_info_obj and hotel_info_obj.telepon:
        context_data['NOMOR_WA_DISPLAY'] = hotel_info_obj.telepon
        temp_wa = hotel_info_obj.telepon.strip().replace('-', '').replace(' ', '').replace('+', '')
        if temp_wa.startswith('08'): context_data['NOMOR_WA_URL'] = '62' + temp_wa[1:]
        elif temp_wa.startswith('62'): context_data['NOMOR_WA_URL'] = temp_wa
        else: context_data['NOMOR_WA_URL'] = temp_wa

    context_data['DATA_INFO_HOTEL_JSON'] = json.dumps(info_data, indent=2)

    # Logika RAG Cerdas
    if 'KAMAR' in intents:
        print("🔍 [RAG] Mengambil data SAMPEL Kamar...")
        tipe_kamar_unik = Kamar.objects.values_list('tipe_kamar', flat=True).distinct()
        kamar_sampel = []
        for tipe in tipe_kamar_unik:
            kamar = Kamar.objects.filter(tipe_kamar=tipe).first()
            if kamar: kamar_sampel.append(kamar)
        kamar_serializer = KamarSerializer(kamar_sampel, many=True)
        context_data['DATA_KAMAR_JSON'] = json.dumps(kamar_serializer.data, indent=2)
        print("ℹ️ [RAG] Data Reservasi sengaja tidak diambil.")

    if 'FASILITAS' in intents:
        print("🔍 [RAG] Mengambil data Fasilitas...")
        fasilitas_objects = FasilitasUmum.objects.all()
        fasilitas_serializer = FasilitasUmumSerializer(fasilitas_objects, many=True)
        context_data['DATA_FASILITAS_JSON'] = json.dumps(fasilitas_serializer.data, indent=2)

    if 'PELAYANAN' in intents:
        print("🔍 [RAG] Mengambil data Pelayanan...")
        pelayanan_objects = Pelayanan.objects.all()
        pelayanan_serializer = PelayananSerializer(pelayanan_objects, many=True)
        context_data['DATA_PELAYANAN_JSON'] = json.dumps(pelayanan_serializer.data, indent=2)

    if 'FAQ' in intents:
        print("🔍 [RAG] Mengambil data FAQ...")
        faq_objects = FAQ.objects.all()
        faq_serializer = FAQSerializer(faq_objects, many=True)
        # Ini adalah perbaikan dari error .data sebelumnya
        context_data['DATA_FAQ_JSON'] = json.dumps(faq_serializer.data, indent=2)

    return context_data

# ... (fungsi build_final_prompt tetap sama) ...

def build_final_prompt(user_message, history, context_data):
    """
    Fungsi RAG - Augmentation (Penambahan).
    Membangun string prompt final dari semua bagian.
    """
    history_formatted = "\n".join([f"{item['role'].replace('model', 'Jaya').replace('user', 'Tamu')}: {item['text']}" for item in history])
    
    # Masukkan data pesan terakhir
    context_data['USER_MESSAGE'] = user_message
    context_data['HISTORY_JSON'] = history_formatted
    
    # Gunakan .format(**dict) untuk mengisi template secara dinamis
    final_prompt = PROMPT_TEMPLATE.format(**context_data)
    return final_prompt