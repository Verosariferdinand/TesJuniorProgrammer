import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastprint_web_django.settings')
django.setup()

from products.models import Kategori, Status, Produk

def seed():
    statuses = ['bisa dijual', 'tidak bisa dijual']
    status_objs = {}
    for s in statuses:
        obj, created = Status.objects.get_or_create(nama_status=s)
        status_objs[s] = obj
    print("Statuses created.")

    categories = ['L QUEENLY', 'L MTH AKSESORIS (IM)', 'Test Category']
    category_objs = {}
    for c in categories:
        obj, created = Kategori.objects.get_or_create(nama_kategori=c)
        category_objs[c] = obj
    print("Categories created.")

    # Create products
    # 1. Product that can be sold
    Produk.objects.get_or_create(
        nama_produk='Test Product Bisa Dijual 1',
        harga=10000,
        kategori=category_objs['L QUEENLY'],
        status=status_objs['bisa dijual']
    )
    
    # 2. Product that cannot be sold
    Produk.objects.get_or_create(
        nama_produk='Test Product Tidak Bisa Dijual',
        harga=5000,
        kategori=category_objs['L MTH AKSESORIS (IM)'],
        status=status_objs['tidak bisa dijual']
    )
    
    # 3. Another product that can be sold
    Produk.objects.get_or_create(
        nama_produk='Test Product Bisa Dijual 2',
        harga=15000,
        kategori=category_objs['Test Category'],
        status=status_objs['bisa dijual']
    )
    
    print("Products created.")

if __name__ == '__main__':
    seed()
