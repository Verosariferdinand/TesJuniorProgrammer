import requests
import mysql.connector

# AMBIL DATA DARI API
res = requests.post(
    "https://recruitment.fastprint.co.id/tes/api_tes_programmer",
    data={
        "username": "tesprogrammer300126C13",
        "password": "62d31365e6f375181dc7da56ff549f3e"
    }
)

json_data = res.json()

if json_data.get("error") != 0:
    print("API ERROR:", json_data)
    exit()

data = json_data["data"]

# KONEKSI DATABASE
db = mysql.connector.connect(
    host="localhost",
    user="fastprint",
    password="fastprintdata",
    database="fastprint"
)

cursor = db.cursor()

# AUTO CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS kategori (
    id_kategori INT AUTO_INCREMENT PRIMARY KEY,
    nama_kategori VARCHAR(255) NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS status (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    nama_status VARCHAR(50) NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id_produk INT PRIMARY KEY,
    nama_produk VARCHAR(255) NOT NULL,
    harga INT NOT NULL,
    kategori_id INT NOT NULL,
    status_id INT NOT NULL,
    CONSTRAINT fk_kategori
        FOREIGN KEY (kategori_id)
        REFERENCES kategori(id_kategori)
        ON UPDATE CASCADE,
    CONSTRAINT fk_status
        FOREIGN KEY (status_id)
        REFERENCES status(id_status)
        ON UPDATE CASCADE
)
""")

# INSERT DATA
for item in data:

    # KATEGORI
    cursor.execute(
        "INSERT IGNORE INTO kategori (nama_kategori) VALUES (%s)",
        (item["kategori"],)
    )
    cursor.execute(
        "SELECT id_kategori FROM kategori WHERE nama_kategori=%s",
        (item["kategori"],)
    )
    kategori_id = cursor.fetchone()[0]

    # STATUS
    cursor.execute(
        "INSERT IGNORE INTO status (nama_status) VALUES (%s)",
        (item["status"],)
    )
    cursor.execute(
        "SELECT id_status FROM status WHERE nama_status=%s",
        (item["status"],)
    )
    status_id = cursor.fetchone()[0]

    # PRODUK
    cursor.execute("""
        INSERT INTO produk
        (id_produk, nama_produk, harga, kategori_id, status_id)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            nama_produk = VALUES(nama_produk),
            harga = VALUES(harga),
            kategori_id = VALUES(kategori_id),
            status_id = VALUES(status_id)
    """, (
        int(item["id_produk"]),
        item["nama_produk"],
        int(item["harga"]),
        kategori_id,
        status_id
    ))

db.commit()
db.close()

print("✅ Database & tabel otomatis dibuat, semua data berhasil disimpan")
