const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'], // Interact well with Django templates
    data() {
        return {
            currentMode: 'bisa_dijual', // 'bisa_dijual' or 'all'
            products: [],
            categories: [],
            statuses: [],
            loading: true,
            
            // Modal State
            showModal: false,
            isEditing: false,
            
            // Form Data
            form: {
                id_produk: null,
                nama_produk: '',
                harga: '',
                kategori_id: null,
                status_id: null
            },
            
            // Helper for special statuses
            statusBisaDijualId: null
        }
    },
    mounted() {
        this.fetchMetadata();
        this.fetchProducts();
    },
    methods: {
        async fetchMetadata() {
            try {
                const response = await axios.get('/api/metadata/');
                this.categories = response.data.categories;
                this.statuses = response.data.statuses;
                
                // Find ID for 'bisa dijual' to set default
                const bisaDijual = this.statuses.find(s => s.nama_status.toLowerCase() === 'bisa dijual');
                if (bisaDijual) {
                    this.statusBisaDijualId = bisaDijual.id_status;
                }
            } catch (error) {
                console.error("Error fetching metadata:", error);
            }
        },
        
        async fetchProducts() {
            this.loading = true;
            try {
                let url = '/api/products/';
                if (this.currentMode === 'bisa_dijual') {
                    url += '?status=bisa%20dijual';
                }
                const response = await axios.get(url);
                this.products = response.data.products;
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Gagal memuat data produk',
                    confirmButtonColor: '#0366d6'
                });
            } finally {
                this.loading = false;
            }
        },
        
        switchMode(mode) {
            this.currentMode = mode;
            this.fetchProducts();
        },
        
        openModal() {
            this.isEditing = false;
            this.showModal = true;
            this.form = {
                id_produk: null,
                nama_produk: '',
                harga: '',
                kategori_id: this.categories.length > 0 ? this.categories[0].id_kategori : null,
                status_id: this.statusBisaDijualId // Default to 'bisa dijual'
            };
            
            // If strict mode, force status
            if (this.currentMode === 'bisa_dijual' && this.statusBisaDijualId) {
                this.form.status_id = this.statusBisaDijualId;
            }
        },
        
        editProduct(product) {
            this.isEditing = true;
            this.showModal = true;
            this.form = { ...product }; // Copy object
        },
        
        closeModal() {
            this.showModal = false;
        },
        
        async saveProduct() {
            const result = await Swal.fire({
                title: `Simpan ${this.isEditing ? 'Perubahan' : 'Data Baru'}?`,
                text: "Pastikan data yang anda masukkan sudah benar.",
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#0366d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Ya, Simpan',
                cancelButtonText: 'Batal'
            });

            if (!result.isConfirmed) return;

            try {
                const payload = { ...this.form };
                
                if (this.isEditing) {
                    await axios.put(`/api/products/${payload.id_produk}/`, payload);
                    Swal.fire({
                        icon: 'success',
                        title: 'Berhasil!',
                        text: 'Data berhasil diubah',
                        confirmButtonColor: '#0366d6'
                    });
                } else {
                    await axios.post('/api/products/', payload);
                    Swal.fire({
                        icon: 'success',
                        title: 'Berhasil!',
                        text: 'Data berhasil ditambahkan',
                        confirmButtonColor: '#0366d6'
                    });
                }
                
                this.closeModal();
                this.fetchProducts();
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Gagal',
                    text: "Terjadi kesalahan: " + (error.response?.data?.error || error.message),
                    confirmButtonColor: '#0366d6'
                });
            }
        },
        
        async confirmDelete(product) {
            // Requirement 5: Alert/Confirmation on delete
            const result = await Swal.fire({
                title: 'Apakah anda yakin?',
                text: `Anda akan menghapus produk "${product.nama_produk}"`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Ya, Hapus!',
                cancelButtonText: 'Batal'
            });

            if (result.isConfirmed) {
                try {
                    await axios.delete(`/api/products/${product.id_produk}/`);
                    Swal.fire({
                        title: 'Terhapus!',
                        text: 'Data berhasil dihapus.',
                        icon: 'success',
                        confirmButtonColor: '#0366d6'
                    });
                    this.fetchProducts();
                } catch (error) {
                    Swal.fire({
                        icon: 'error',
                        title: 'Gagal',
                        text: 'Gagal menghapus data',
                        confirmButtonColor: '#0366d6'
                    });
                }
            }
        },
        
        // Utils
        formatPrice(value) {
            return new Intl.NumberFormat('id-ID').format(value);
        },
        
        getStatusClass(statusName) {
            return statusName.toLowerCase() === 'bisa dijual' ? 'status-ok' : 'status-bad';
        }
    }
}).mount('#app');
