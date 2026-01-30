import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Produk, Kategori, Status

def vue_app(request):
    """Render the main Vue.js SPA entry point."""
    return render(request, 'products/index.html')

def api_metadata(request):
    """Return categories and statuses for dropdowns."""
    categories = list(Kategori.objects.values('id_kategori', 'nama_kategori'))
    statuses = list(Status.objects.values('id_status', 'nama_status'))
    return JsonResponse({'categories': categories, 'statuses': statuses})

@csrf_exempt
def api_product_list(request):
    """API for listing and creating products."""
    if request.method == 'GET':
        status_filter = request.GET.get('status')
        products_qs = Produk.objects.select_related('kategori', 'status').all()
        
        if status_filter:
            products_qs = products_qs.filter(status__nama_status__iexact=status_filter)
            
        products = []
        for p in products_qs:
            products.append({
                'id_produk': p.id_produk,
                'nama_produk': p.nama_produk,
                'harga': p.harga,
                'kategori_id': p.kategori.id_kategori,
                'kategori_nama': p.kategori.nama_kategori,
                'status_id': p.status.id_status,
                'status_nama': p.status.nama_status,
            })
        return JsonResponse({'products': products})
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Basic Validation
            if not data.get('nama_produk'):
                return JsonResponse({'error': 'Nama produk wajib diisi!'}, status=400)
            if not str(data.get('harga')).isdigit():
                return JsonResponse({'error': 'Harga harus berupa angka!'}, status=400)
                
            kategori = get_object_or_404(Kategori, pk=data.get('kategori_id'))
            status = get_object_or_404(Status, pk=data.get('status_id'))
            
            product = Produk.objects.create(
                nama_produk=data['nama_produk'],
                harga=data['harga'],
                kategori=kategori,
                status=status
            )
            return JsonResponse({'message': 'Produk berhasil ditambahkan!', 'id': product.id_produk}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def api_product_detail(request, pk):
    """API for updating and deleting a product."""
    product = get_object_or_404(Produk, pk=pk)
    
    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'message': 'Produk berhasil dihapus!'})
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            # Basic Validation
            if not data.get('nama_produk'):
                return JsonResponse({'error': 'Nama produk wajib diisi!'}, status=400)
            if not str(data.get('harga')).isdigit():
                return JsonResponse({'error': 'Harga harus berupa angka!'}, status=400)
            
            kategori = get_object_or_404(Kategori, pk=data.get('kategori_id'))
            status = get_object_or_404(Status, pk=data.get('status_id'))
            
            product.nama_produk = data['nama_produk']
            product.harga = data['harga']
            product.kategori = kategori
            product.status = status
            product.save()
            
            return JsonResponse({'message': 'Produk berhasil diupdate!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
