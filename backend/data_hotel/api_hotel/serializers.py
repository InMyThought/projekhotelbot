# api_hotel/serializers.py

from rest_framework import serializers
from .models import Kamar, FAQ, FasilitasUmum, Pelayanan, HotelInfo,Reservasi

class KamarSerializer(serializers.ModelSerializer):
    status_ketersediaan = serializers.SerializerMethodField()
    harga_setelah_diskon = serializers.SerializerMethodField()

    class Meta:
        model = Kamar
        fields = [
            'id', 'nomor_kamar', 'tipe_kamar', 'harga_per_malam', 
            'kapasitas', 'fasilitas', 'status_ketersediaan',
            'diskon_persen', 'catatan_diskon', 'harga_setelah_diskon',
            'url_gambar' # Menambahkan field gambar
        ]

    def get_status_ketersediaan(self, obj):
        return "Tersedia" if obj.is_available_now() else "Tidak Tersedia"
    
    def get_harga_setelah_diskon(self, obj):
        if obj.diskon_persen > 0:
            harga_asli = obj.harga_per_malam
            potongan = (harga_asli * obj.diskon_persen) / 100
            harga_final = harga_asli - potongan
            return f"{harga_final:.2f}"
        return None

class ReservasiSerializer(serializers.ModelSerializer):
    # Serializer ini tidak perlu kita ubah untuk sekarang
   class Meta:
        model = Reservasi
        # HANYA sertakan field yang dibutuhkan AI untuk cek ketersediaan
        fields = ['kamar', 'tanggal_check_in', 'tanggal_check_out']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class FasilitasUmumSerializer(serializers.ModelSerializer):
    class Meta:
        model = FasilitasUmum
        fields = '__all__'

class PelayananSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pelayanan
        fields = '__all__'

class HotelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInfo
        fields = "__all__"

