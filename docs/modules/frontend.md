# Module Frontend

## Cấu trúc thư mục

```
frontend/src/
├── assets/          # CSS global, hình ảnh tĩnh
├── components/      # Component tái sử dụng
│   ├── Navbar.vue       # Thanh điều hướng + mega menu
│   ├── CartSidebar.vue  # Giỏ hàng trượt ra
│   ├── ProductCard.vue  # Card sản phẩm
│   ├── AppFooter.vue    # Footer
│   └── ToastContainer.vue # Thông báo toast
├── views/           # Trang chính
│   ├── Home.vue         # Trang chủ
│   ├── Products.vue     # Danh sách sản phẩm
│   ├── ProductDetail.vue # Chi tiết sản phẩm
│   ├── Cart.vue         # Giỏ hàng + thanh toán
│   ├── Login.vue        # Đăng nhập / Đăng ký
│   ├── Profile.vue      # Trang cá nhân
│   ├── Wishlist.vue     # Sản phẩm yêu thích
│   ├── Collections.vue  # Bộ sưu tập
│   └── admin/           # Trang quản trị
│       ├── Dashboard.vue
│       ├── Orders.vue
│       ├── Products.vue
│       ├── Customers.vue
│       ├── Categories.vue
│       └── Stats.vue
├── layouts/         # Layout wrapper
│   ├── DefaultLayout.vue  # Layout người dùng
│   └── AdminLayout.vue    # Layout admin
├── stores/          # Pinia stores
│   ├── cart.js      # Quản lý giỏ hàng
│   ├── auth.js      # Xác thực người dùng
│   ├── wishlist.js  # Danh sách yêu thích
│   └── toast.js     # Thông báo
├── services/        # Gọi API
│   ├── api.js           # Axios instance + interceptors
│   ├── productService.js
│   ├── orderService.js
│   └── authService.js
├── composables/     # Logic tái sử dụng
│   ├── useProducts.js
│   └── useSearch.js
├── utils/           # Hàm tiện ích
│   └── format.js    # formatPrice, discountPercent
├── router/
│   └── index.js     # Định nghĩa routes
└── data/
    └── products.js  # Mock data cho admin dashboard
```

## Stores (Pinia)

### `cart.js`
- Lưu giỏ hàng vào `localStorage`
- Actions: `addItem`, `removeItem`, `updateQuantity`, `clearCart`

### `auth.js`
- Lưu token và user vào `localStorage`
- Hỗ trợ đăng nhập Email và Google OAuth
- Actions: `login`, `register`, `loginWithGoogle`, `logout`

### `wishlist.js`
- Lưu sản phẩm yêu thích vào `localStorage`
- Actions: `toggle`, `remove`

### `toast.js`
- Hiển thị thông báo tạm thời
- Methods: `success`, `error`, `info`

## Routes

| Path | Component | Mô tả |
|------|-----------|-------|
| `/` | Home | Trang chủ |
| `/products` | Products | Danh sách sản phẩm |
| `/products/:id` | ProductDetail | Chi tiết sản phẩm |
| `/cart` | Cart | Giỏ hàng |
| `/login` | Login | Đăng nhập/Đăng ký |
| `/profile` | Profile | Trang cá nhân |
| `/wishlist` | Wishlist | Yêu thích |
| `/collections` | Collections | Bộ sưu tập |
| `/admin` | Dashboard | Admin dashboard |
| `/admin/orders` | Orders | Quản lý đơn hàng |
| `/admin/products` | Products | Quản lý sản phẩm |
| `/admin/customers` | Customers | Quản lý khách hàng |
| `/admin/categories` | Categories | Quản lý danh mục |
| `/admin/stats` | Stats | Thống kê |
