# api_hotel/models.py

from django.db import models
from django.utils import timezone

class Kamar(models.Model):
    nomor_kamar = models.CharField(max_length=10, unique=True)
    
    TIPE_KAMAR_CHOICES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]
    
    tipe_kamar = models.CharField(max_length=50, choices=TIPE_KAMAR_CHOICES, default='Standard')
    harga_per_malam = models.DecimalField(max_digits=10, decimal_places=2)
    kapasitas = models.IntegerField(default=2, help_text="Jumlah maksimal tamu")
    fasilitas = models.TextField(help_text="Fasilitas di kamar, pisahkan dengan koma")
    
    # Field untuk diskon
    diskon_persen = models.IntegerField(default=0, help_text="Diskon dalam persen, misal: 15 untuk 15%")
    catatan_diskon = models.CharField(max_length=255, blank=True, null=True, help_text="Contoh: Promo Akhir Pekan!")

    # Field untuk fitur "Kirim Foto" (Fitur Bonus)
    url_gambar = models.URLField(max_length=500, blank=True, null=True, help_text="URL gambar kamar yang bisa diakses publik")
    
    def __str__(self):
        return f"Kamar {self.nomor_kamar} ({self.tipe_kamar})"

    def is_available_now(self):
        sekarang = timezone.now()
        reservasi_aktif = self.reservasi_set.filter(
            tanggal_check_in__lte=sekarang,
            tanggal_check_out__gte=sekarang
        ).exists()
        return not reservasi_aktif

class Reservasi(models.Model):
    kamar = models.ForeignKey(Kamar, on_delete=models.CASCADE)
    nama_tamu = models.CharField(max_length=100)
    tanggal_check_in = models.DateTimeField()
    tanggal_check_out = models.DateTimeField()

    def __str__(self):
        return f"Reservasi {self.kamar.nomor_kamar} oleh {self.nama_tamu}"

class FAQ(models.Model):
    pertanyaan = models.CharField(max_length=255)
    jawaban = models.TextField()
    kategori = models.CharField(max_length=100, blank=True, null=True, help_text="Contoh: fasilitas, reservasi, umum")

    def __str__(self):
        return self.pertanyaan

class FasilitasUmum(models.Model):
    nama_fasilitas = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    jam_buka = models.CharField(max_length=50, blank=True, null=True)
    lokasi = models.CharField(max_length=100, blank=True, null=True)
    gambar_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nama_fasilitas

class Pelayanan(models.Model):
    nama_layanan = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    biaya = models.DecimalField(max_digits=10, decimal_places=2, help_text="Biaya layanan (Rp)")
    jam_operasional = models.CharField(max_length=50, blank=True, null=True)
    gambar_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nama_layanan

class HotelInfo(models.Model):
    nama = models.CharField(max_length=200, default="Hotel Maju Jaya")
    alamat = models.TextField(blank=True, null=True)
    kota = models.CharField(max_length=100, blank=True, null=True)
    negara = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    telepon = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(max_length=300, blank=True, null=True, help_text="URL website resmi hotel, misal: https://www.hotelmajujaya.com")
    email = models.EmailField(blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    jam_check_in = models.TimeField(blank=True, null=True)
    jam_check_out = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Informasi Hotel"
        verbose_name_plural = "Informasi Hotel"

    def __str__(self):
        return self.nama

