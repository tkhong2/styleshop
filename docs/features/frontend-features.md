# Tính năng Frontend

## Trang người dùng

### Trang chủ (`/`)
- Hero slider tự động (3 slides, 5 giây/slide)
- Flash Sale với countdown timer đếm ngược
- Danh mục icon (6 danh mục)
- Section hàng mới về, đang giảm giá
- Banner strip 3 cột (Giày, Túi, Quần áo)
- Tab sản phẩm theo danh mục (Áo/Quần/Váy)
- Bộ sưu tập (Collections)
- Benefits section (vận chuyển, đổi trả, bảo hành, thanh toán)
- Popup khuyến mãi (hiện sau 3 giây, 1 lần/session, mã NEWUSER)

### Trang sản phẩm (`/products`)
- Filter: danh mục, giới tính, khoảng giá (range slider), sale/mới
- Sắp xếp: mặc định, giá tăng/giảm, đánh giá, mới nhất
- Phân trang 12 sản phẩm/trang
- Skeleton loading
- Lịch sử xem gần đây (10 sản phẩm)
- Quick View popup (chọn size/màu, thêm giỏ ngay)
- Nút reset bộ lọc

### Trang chi tiết sản phẩm (`/products/:id`)
- Gallery ảnh với thumbnail
- Chọn màu sắc, kích thước
- Nút thêm giỏ hàng + yêu thích
- Chia sẻ Facebook + copy link
- Sản phẩm liên quan (4 sản phẩm cùng danh mục)
- Lưu lịch sử xem tự động

### Giỏ hàng (`/cart`)
- Cập nhật số lượng, xóa sản phẩm
- Mã giảm giá (STYLE10, SALE20, NEWUSER)
- Phí vận chuyển tự động
- 3 phương thức thanh toán:
  - Chuyển khoản BIDV (VietQR + SePay webhook)
  - Ví MoMo
  - COD với form địa chỉ giao hàng
- Polling tự động 5 giây chờ xác nhận thanh toán
- Modal thành công sau khi thanh toán

### Đăng nhập/Đăng ký (`/login`)
- Tab đăng nhập / đăng ký
- Google OAuth (Google Identity Services)
- Redirect admin tự động nếu email admin

### Trang cá nhân (`/profile`)
- Tab: Đơn hàng, Thông tin, Yêu thích
- Lịch sử đơn hàng theo user
- Cập nhật thông tin cá nhân

### Wishlist (`/wishlist`)
- Lưu localStorage
- Hiển thị dạng grid sản phẩm

### Bộ sưu tập (`/collections`, `/collections/:slug`)
- 6 bộ sưu tập với ảnh và mô tả

### Trang hỗ trợ
- `/huong-dan-chon-size` — Bảng size áo, quần, váy + cách đo
- `/cau-hoi-thuong-gap` — FAQ có tìm kiếm + accordion
- `/chinh-sach-doi-tra` — Điều kiện, quy trình đổi trả
- `/thanh-toan-giao-nhan` — Phí ship, phương thức, quy trình
- `/chinh-sach-bao-mat` — Chính sách bảo mật đầy đủ

---

## Trang Admin (`/admin/*`)

> Chỉ tài khoản `khachong2102005@gmail.com` mới truy cập được

### Dashboard (`/admin`)
- 4 stat cards với sparkline chart (dữ liệu thật từ API)
- Biểu đồ doanh thu 7 ngày (Line chart)
- Bảng đơn hàng gần đây
- Top 5 sản phẩm bán chạy
- Doughnut chart trạng thái đơn hàng
- Quick stats tổng quan

### Đơn hàng (`/admin/orders`)
- Bảng đơn hàng thật từ API
- Filter: tìm kiếm, trạng thái, phương thức
- Xác nhận thanh toán thủ công (nút ✓)
- Xuất CSV
- Tóm tắt: tổng đơn, đã TT, chờ TT, doanh thu

### Sản phẩm (`/admin/products`)
- Danh sách 100 sản phẩm từ API
- Filter: tìm kiếm, danh mục, giới tính
- Phân trang 15 sản phẩm/trang

### Khách hàng (`/admin/customers`)
- Danh sách khách hàng (mock)
- Hiển thị provider (Google/Email)
- Tóm tắt: tổng, hoạt động, mới, Google

### Danh mục (`/admin/categories`)
- Danh sách danh mục với progress bar
- Form thêm danh mục mới

### Mã giảm giá (`/admin/coupons`)
- Danh sách coupon với trạng thái
- Thêm/xóa/bật-tắt coupon
- Hỗ trợ: phần trăm và số tiền cố định

### Thống kê (`/admin/stats`)
- KPI cards (dữ liệu thật)
- Biểu đồ doanh thu theo ngày (Line)
- Biểu đồ số đơn hàng (Bar)
- Doughnut danh mục
- Phương thức thanh toán (progress bar)

### Trang cá nhân admin (`/admin/profile`)
- Thông tin tài khoản + đổi mật khẩu
- Thống kê nhanh (tổng đơn, doanh thu, đã TT)
- Lịch sử hoạt động

---

## Components

| Component | Mô tả |
|-----------|-------|
| `Navbar.vue` | Mega menu, tìm kiếm realtime với gợi ý, mobile drawer |
| `BottomNav.vue` | Bottom navigation bar cho mobile |
| `CartSidebar.vue` | Giỏ hàng slide-out |
| `ProductCard.vue` | Card sản phẩm với wishlist, quick view |
| `QuickView.vue` | Popup xem nhanh sản phẩm |
| `PromoPopup.vue` | Popup khuyến mãi (1 lần/session) |
| `ToastContainer.vue` | Thông báo toast |
| `AppFooter.vue` | Footer với links hỗ trợ |

## Stores (Pinia)

| Store | Mô tả |
|-------|-------|
| `cart.js` | Giỏ hàng, persist localStorage |
| `auth.js` | Xác thực, Google OAuth |
| `wishlist.js` | Yêu thích, persist localStorage |
| `toast.js` | Thông báo |
| `history.js` | Lịch sử xem sản phẩm |

## Mobile Optimization
- Bottom Navigation Bar (Home, Sản phẩm, Giỏ hàng, Yêu thích, Tài khoản)
- Touch targets tối thiểu 44px
- Font size input 16px (tránh iOS zoom)
- Payment modal bottom sheet trên mobile
- Ẩn topbar trên mobile
- Safe area cho iPhone notch
