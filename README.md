# Aplikasi Manajemen Produk FastPrint

Website sederhana untuk mengelola data produk dengan filter status "Bisa Dijual", dibuat menggunakan **Django (Backend)** dan **Vue.js (Frontend)**.

## Fitur Utama

- **Dua Mode Tampilan**:
  - **Mode "Bisa Dijual"**: Hanya menampilkan produk yang bisa dijual.
  - **Mode "Semua Data"**: Menampilkan semua produk untuk keperluan administrasi.
- **Manajemen Data (CRUD)**:
  - Tambah Produk Baru.
  - Edit Produk yang sudah ada.
  - Hapus Produk (dengan konfirmasi aman).
- **Desain Modern**: Antarmuka bersih dengan tema dominan putih dan efek interaktif (Glassmorphism halus).
- **Alert Interaktif**: Menggunakan SweetAlert2 untuk notifikasi yang menarik.

## Persyaratan Sistem

- Python 3.10 atau lebih baru
- MySQL Database

## Cara Instalasi

1.  **Clone Repository** (jika ada) atau ekstrak folder project.
2.  **Buat Virtual Environment** (opsional tapi disarankan):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Untuk Linux/Mac
    # venv\Scripts\activate   # Untuk Windows
    ```
3.  **Install Library yang Dibutuhkan**:
    ```bash
    pip install -r requirements.txt
    ```

## Konfigurasi Database

1.  Pastikan service MySQL Anda sudah berjalan.
2.  Buat database baru bernama `fastprint` di MySQL Anda.
3.  Buka file `fastprint_web_django/settings.py` dan sesuaikan konfigurasi database jika username/password Anda berbeda:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'fastprint',
            'USER': '',      # Ganti dengan user database Anda
            'PASSWORD': '',      # Isikan password jika ada
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```
4.  Jalankan migrasi untuk membuat tabel:
    ```bash
    python manage.py migrate
    ```

## Cara Menjalankan Aplikasi

Jalankan perintah berikut di terminal:

```bash
python manage.py runserver
```

Buka browser dan akses alamat: `http://127.0.0.1:8000`

## Struktur Project

- `products/`: Aplikasi utama Django yang menangani data produk.
- `products/static/products/app.js`: Logika Frontend menggunakan Vue.js.
- `products/templates/products/index.html`: Halaman utama aplikasi.
