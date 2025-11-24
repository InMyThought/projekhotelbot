from django.contrib import admin

# Register your models here.
from .models import Kamar, Reservasi, FAQ, FasilitasUmum, Pelayanan,HotelInfo

# Kode ini memberitahu Django untuk menampilkan
# model Kamar dan Reservasi di halaman admin.
admin.site.register(Kamar)
admin.site.register(Reservasi)
admin.site.register(FAQ)
admin.site.register(FasilitasUmum)
admin.site.register(Pelayanan)
admin.site.register(HotelInfo)