# # api_hotel/views.py

# import os
# import json
# import requests
# from dotenv import load_dotenv
# from django.utils import timezone 

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from .models import Kamar, FAQ, FasilitasUmum, Pelayanan, HotelInfo, Reservasi
# # === DIUBAH: Impor kembali ReservasiSerializer ===
# from .serializers import (
#     KamarSerializer, FAQSerializer, FasilitasUmumSerializer, 
#     PelayananSerializer, HotelInfoSerializer, 
#     ReservasiSerializer  # <-- Kembali ke serializer asli
# )

# # --- KONFIGURASI ---
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# # --- PROMPT TEMPLATE UTAMA (Tetap dengan Aturan Privasi) ---
# PROMPT_TEMPLATE = """
# # 1. PERSONA
# Anda adalah "Jaya", Resepsionis AI dari Hotel Maju Jaya. Nada bicara Anda profesional, ramah, dan sangat membantu. Gunakan Bahasa Indonesia.

# # 2. SUMBER PENGETAHUAN
# Anda HANYA boleh menjawab berdasarkan [DATA KAMAR], [DATA RESERVASI AKTIF], dan [INFO HOTEL & FAQ].
# Nomor Telepon Resepsionis (juga nomor WA) adalah: {NOMOR_WA_DISPLAY}.

# # 3. ATURAN JAWABAN
# - Ubah data JSON menjadi kalimat percakapan yang natural.
# - Jika sebuah kamar punya diskon (`diskon_persen` > 0), UMUMKAN DISKON ITU SECARA PROAKTIF.
# - Gunakan [DATA RESERVASI AKTIF] untuk mengecek ketersediaan tanggal.

# # 4. ATURAN PRIVASI & KEAMANAN (SANGAT PENTING!)
# - Anda TIDAK MEMILIKI AKSES ke nama tamu yang sedang menginap.
# - Jika ada yang bertanya siapa yang sedang menginap, JAWAB DENGAN TEGAS: "Mohon maaf, demi menjaga privasi dan keamanan seluruh tamu kami, saya tidak bisa memberikan informasi tersebut."

# # 5. ATURAN KHUSUS: RESERVASI & CHECK-IN
# - Jika tamu ingin MEMBUAT RESERVASI, bantu kumpulkan datanya dan buatkan tautan `https://wa.me/` menggunakan {NOMOR_WA_URL}.
# - Anda BUKAN resepsionis di lobi. Anda tidak bisa melakukan Check-in atau Check-out.

# # === PERUBAHAN DI BAWAH INI ===
# - Jika tamu meminta untuk "check-in" atau "check-out" (misal: "Saya mau check-in sekarang"), arahkan tamu ke lobi.
# - Jika tamu bertanya "BAGAIMANA LANGKAH check-in?" atau "Prosedur check-in?", jelaskan singkat (perlu ke lobi, siapkan KTP) DAN BERIKAN NOMOR TELEPON RESEPSIONIS ({NOMOR_WA_DISPLAY}) untuk konfirmasi.

# # CONTOH PENANGANAN RESERVASI:
# Tamu: "Saya mau pesan kamar Suite dong."
# Jaya: "Tentu, ... (proses pengumpulan data) ... https://wa.me/{NOMOR_WA_URL}?text=Halo%20Admin%2C%20..."

# # === CONTOH BARU DI BAWAH INI ===
# # CONTOH PENANGANAN LANGKAH CHECK-IN:
# Tamu: "Bagaimana langkah-langkah check-in?"
# Jaya: "Tentu. Untuk proses check-in, silakan langsung menuju meja resepsionis di lobi hotel kami. Mohon siapkan KTP atau identitas diri Anda yang valid. Jika Anda memerlukan bantuan atau ingin konfirmasi kedatangan, Anda bisa menghubungi resepsionis kami di nomor {NOMOR_WA_DISPLAY}. Selamat beristirahat!"

# # [DATA KAMAR]
# {DATA_KAMAR_JSON}

# # [DATA RESERVASI AKTIF] (Otomatis aman, tanpa nama tamu)
# {DATA_RESERVASI_JSON}

# # [INFO HOTEL & FAQ]
# {INFO_HOTEL_JSON}
# ---
# # RIWAYAT PERCAKAPAN
# {HISTORY_JSON}

# # PERCAKAPAN SAAT INI
# Tamu: "{USER_MESSAGE}"
# Jawaban Anda (Jaya):
# """
# # --- FUNGSI HELPER ---
# # ... (call_gemini_api tetap sama) ...
# def call_gemini_api(prompt):
#     if not GEMINI_API_KEY:
#         return "Sistem AI tidak terkonfigurasi."
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
#     payload = {"contents": [{"parts": [{"text": prompt}]}]}
#     try:
#         response = requests.post(url, json=payload, timeout=30) 
#         response.raise_for_status()
#         data = response.json()
#         return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
#     except requests.exceptions.RequestException as e:
#         print(f"⚠️ Gemini error: {e}")
#         return None

# # --- "OTAK" UTAMA CHATBOT ---
# class ChatbotAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         # ... (logika mengambil user_message dan history tetap sama) ...
#         user_message = request.data.get('message')
#         history_str = request.data.get('history', '[]')
#         try:
#             history = json.loads(history_str)
#         except json.JSONDecodeError:
#             return Response({"error": "Format 'history' tidak valid."}, status=status.HTTP_400_BAD_REQUEST)
#         if not user_message:
#             return Response({"error": "Parameter 'message' diperlukan."}, status=status.HTTP_400_BAD_REQUEST)

#         # ... (logika mengambil data kamar tetap sama) ...
#         kamar_objects = Kamar.objects.all()
#         kamar_serializer = KamarSerializer(kamar_objects, many=True)
#         data_kamar_json = json.dumps(kamar_serializer.data, indent=2)

#         # 2. Ambil data reservasi dinamis
#         sekarang = timezone.now()
#         reservasi_objects = Reservasi.objects.filter(tanggal_check_out__gte=sekarang)
        
#         # === DIUBAH: Gunakan Serializer Asli (yang sudah aman) ===
#         reservasi_serializer = ReservasiSerializer(reservasi_objects, many=True)
#         data_reservasi_json = json.dumps(reservasi_serializer.data, indent=2)
#         # ========================================================

#         # ... (sisa logika mengambil info hotel, no WA, dll tetap sama) ...
        
#         # 3. Siapkan data info hotel & FAQ statis
#         # ... (kode ini tetap sama) ...
#         faq_objects = FAQ.objects.all()
#         faq_serializer = FAQSerializer(faq_objects, many=True)
#         fasilitas_objects = FasilitasUmum.objects.all()
#         fasilitas_serializer = FasilitasUmumSerializer(fasilitas_objects, many=True)
#         pelayanan_objects = Pelayanan.objects.all()
#         pelayanan_serializer = PelayananSerializer(pelayanan_objects, many=True)
#         hotel_info_obj = HotelInfo.objects.first()
#         hotel_info_serializer = HotelInfoSerializer(hotel_info_obj) if hotel_info_obj else None
        
#         # 4. Ambil Nomor WhatsApp
#         # ... (kode ini tetap sama) ...
#         nomor_wa_display = "Nomor WhatsApp tidak tersedia"
#         nomor_wa_url = "" 
#         if hotel_info_obj and hotel_info_obj.telepon:
#             nomor_wa_display = hotel_info_obj.telepon
#             temp_wa = hotel_info_obj.telepon.strip().replace('-', '').replace(' ', '').replace('+', '')
#             if temp_wa.startswith('08'):
#                 nomor_wa_url = '62' + temp_wa[1:]
#             elif temp_wa.startswith('62'):
#                 nomor_wa_url = temp_wa
#             else:
#                 nomor_wa_url = temp_wa
        
#         info_hotel = {
#             "info_umum": hotel_info_serializer.data if hotel_info_serializer else {}, # <--- INFO UMUM MASUK
#             "faq": faq_serializer.data,
#             "fasilitas_umum": fasilitas_serializer.data, # <--- FASILITAS MASUK
#             "pelayanan_hotel": pelayanan_serializer.data
#         }
#         info_hotel_json = json.dumps(info_hotel, indent=2)
#         history_formatted = "\n".join([f"{item['role'].replace('model', 'Jaya').replace('user', 'Tamu')}: {item['text']}" for item in history])

#         # 5. Bangun prompt final
#         final_prompt = PROMPT_TEMPLATE.format(
#             # ... (semua variabel format tetap sama) ...
#             DATA_KAMAR_JSON=data_kamar_json,
#             DATA_RESERVASI_JSON=data_reservasi_json, 
#             INFO_HOTEL_JSON=info_hotel_json,
#             HISTORY_JSON=history_formatted,
#             USER_MESSAGE=user_message,
#             NOMOR_WA_DISPLAY=nomor_wa_display, 
#             NOMOR_WA_URL=nomor_wa_url
#         )
        
#         # 6. Panggil Gemini
#         ai_response = call_gemini_api(final_prompt) or "Mohon maaf, sistem sedang mengalami kendala."

#         return Response({"reply": ai_response}, status=status.HTTP_200_OK)



# api_hotel/views.py
import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Kamar, FAQ, FasilitasUmum, Pelayanan, HotelInfo, Reservasi
from .serializers import (
    KamarSerializer, FAQSerializer, FasilitasUmumSerializer, 
    PelayananSerializer, HotelInfoSerializer, ReservasiSerializer
)
from .rag_router import get_intents_from_message, retrieve_context_data, build_final_prompt

try:
    from .kalkulator import buat_reservasi
except ImportError:
    def buat_reservasi(*args, **kwargs):
        return {"status": "Error", "message": "Modul kalkulator.py tidak ditemukan."}

load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

def call_gemini_api(prompt):
    if not GEMINI_API_KEY:
        return "Sistem AI tidak terkonfigurasi."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=30) 
        response.raise_for_status()
        data = response.json()
        return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Gemini error: {e}")
        return None

# OTAK 1: UNTUK CHATBOT WHATSAPP (RAG)
class ChatbotAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        history_str = request.data.get('history', '[]')
        try:
            history = json.loads(history_str)
        except json.JSONDecodeError:
            return Response({"error": "Format 'history' tidak valid."}, status=status.HTTP_400_BAD_REQUEST)
        if not user_message:
            return Response({"error": "Parameter 'message' diperlukan."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            intents = get_intents_from_message(user_message)
            print(f"💡 [RAG] Intents terdeteksi: {intents}")
            context_data = retrieve_context_data(intents)
            final_prompt = build_final_prompt(user_message, history, context_data)
        except Exception as e:
            print(f"🔥 [RAG LOGIC ERROR] Terjadi error di rag_router: {e}")
            ai_response = "Mohon maaf, terjadi kesalahan internal saat memproses data hotel kami. Silakan coba lagi."
            return Response({"reply": ai_response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        ai_response = call_gemini_api(final_prompt) or "Mohon maaf, sistem sedang mengalami kendala."
        return Response({"reply": ai_response}, status=status.HTTP_200_OK)

# OTAK 2: UNTUK HALAMAN VIEWER UTAMA (/)
def hotel_viewer_view(request):
    kamar_list = Kamar.objects.all().order_by('nomor_kamar')
    fasilitas_list = FasilitasUmum.objects.all()
    pelayanan_list = Pelayanan.objects.all()
    hotel_info = HotelInfo.objects.first()
    
    context = {
        'kamar_list': kamar_list,
        'fasilitas_list': fasilitas_list,
        'pelayanan_list': pelayanan_list,
        'hotel_info': hotel_info,
        'title': 'Viewer Hotel'
    }
    return render(request, 'hotel_viewer.html', context)

# OTAK 3: UNTUK APLIKASI RESERVASI (/kamar/)
def kamar_list_view(request):
    kamar_list = Kamar.objects.all().order_by('nomor_kamar')
    tipe_kamar_list = Kamar.objects.values_list('tipe_kamar', flat=True).distinct()
    
    hasil_cek = None
    form_values = {} 
    if request.method == "POST":
        cek_tipe = request.POST.get('tipe_kamar')
        cek_in_str = request.POST.get('check_in')
        cek_out_str = request.POST.get('check_out')
        nama_tamu = request.POST.get('nama_tamu')
        
        form_values = request.POST 

        if cek_tipe and cek_in_str and cek_out_str and nama_tamu:
            try:
                tgl_check_in = datetime.strptime(cek_in_str, "%Y-%m-%d").date()
                tgl_check_out = datetime.strptime(cek_out_str, "%Y-%m-%d").date()
                
                if tgl_check_out <= tgl_check_in:
                     hasil_cek = {"status": "Error", "message": "Tanggal check-out harus setelah tanggal check-in."}
                else:
                    hasil_cek = buat_reservasi(cek_tipe, tgl_check_in, tgl_check_out, nama_tamu)
            except ValueError:
                hasil_cek = {"status": "Error", "message": "Format tanggal tidak valid."}
        else:
            hasil_cek = {"status": "Error", "message": "Semua field (Nama, Tipe, Tanggal) wajib diisi."}

    context = {
        'kamar_list': kamar_list,
        'tipe_kamar_list': tipe_kamar_list,
        'hasil_cek': hasil_cek,
        'form_values': form_values
    }
    return render(request, 'kamar_list.html', context)