import sqlite3

# koneksi ke database Django
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# baca isi file SQL
with open('seed_hotel.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# jalankan seluruh isi file
cursor.executescript(sql_script)
conn.commit()
conn.close()

print("✅ Data berhasil diimport ke database.")
