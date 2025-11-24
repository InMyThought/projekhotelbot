# api_hotel/kalkulator.py
from .models import Kamar, Reservasi
from django.db.models import Q

def check_availability_kalkulator(tipe_kamar, tanggal_check_in, tanggal_check_out):
    # ... (Fungsi ini tidak kita pakai, kita pakai 'buat_reservasi') ...
    pass

def buat_reservasi(tipe_kamar, tanggal_check_in, tanggal_check_out, nama_tamu):
    """
    Eksekutor hardcode untuk MENGECEK dan LANGSUNG MEMBUAT reservasi.
    """
    try:
        if not nama_tamu or nama_tamu.strip() == "":
            return {"status": "Error", "message": "Nama tamu tidak boleh kosong."}

        kamar_tersedia_tipe_ini = Kamar.objects.filter(tipe_kamar__iexact=tipe_kamar)
        if not kamar_tersedia_tipe_ini.exists():
            return {"status": "Error", "message": f"Tipe kamar '{tipe_kamar}' tidak ditemukan."}

        reservasi_bentrok = Reservasi.objects.filter(
            kamar__in=kamar_tersedia_tipe_ini,
            tanggal_check_in__lt=tanggal_check_out,
            tanggal_check_out__gt=tanggal_check_in
        )
        kamar_bentrok_ids = reservasi_bentrok.values_list('kamar__id', flat=True)
        kamar_yang_benar_tersedia = kamar_tersedia_tipe_ini.exclude(id__in=kamar_bentrok_ids)

        if kamar_yang_benar_tersedia.exists():
            kamar_untuk_dipesan = kamar_yang_benar_tersedia.first()
            
            reservasi_baru = Reservasi(
                kamar=kamar_untuk_dipesan,
                nama_tamu=nama_tamu,
                tanggal_check_in=tanggal_check_in,
                tanggal_check_out=tanggal_check_out
            )
            reservasi_baru.save()
            
            return {
                "status": "Sukses",
                "message": f"Reservasi atas nama {nama_tamu} untuk Kamar {kamar_untuk_dipesan.nomor_kamar} ({tipe_kamar}) berhasil dibuat."
            }
        else:
            return {
                "status": "Penuh",
                "tipe_kamar": tipe_kamar,
                "check_in": tanggal_check_in.strftime("%Y-%m-%d"),
                "check_out": tanggal_check_out.strftime("%Y-%m-%d")
            }
            
    except Exception as e:
        print(f"🔥 Error di Eksekutor Reservasi: {e}")
        return {"status": "Error", "message": str(e)}