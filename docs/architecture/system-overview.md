# Kiến trúc hệ thống

## Sơ đồ tổng quan

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT                              │
│  Browser → Vue 3 SPA (Vercel)                           │
│  - Pinia (State Management)                             │
│  - Vue Router (Routing)                                 │
│  - Axios (HTTP Client)                                  │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTPS
┌──────────────────────▼──────────────────────────────────┐
│                   BACKEND                                │
│  FastAPI (Render.com)                                   │
│  - REST API                                             │
│  - SQLite Database                                      │
│  - CORS Middleware                                      │
└──────────────────────┬──────────────────────────────────┘
                       │ Webhook
┌──────────────────────▼──────────────────────────────────┐
│               THIRD-PARTY SERVICES                       │
│  - SePay (Thanh toán ngân hàng BIDV)                   │
│  - VietQR (Tạo mã QR thanh toán)                       │
│  - Google OAuth (Đăng nhập)                             │
└─────────────────────────────────────────────────────────┘
```

## Luồng dữ liệu chính

### 1. Luồng mua hàng
```
User → Chọn sản phẩm → Thêm giỏ hàng (localStorage)
     → Thanh toán → Tạo đơn hàng (POST /api/orders)
     → Chuyển khoản → SePay webhook → Cập nhật trạng thái
     → Frontend polling → Hiển thị thành công
```

### 2. Luồng xác thực
```
User → Đăng nhập (Email/Google)
     → JWT Token lưu localStorage
     → Axios interceptor gắn token vào mọi request
```

## Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend Framework | Vue.js | 3.4 |
| State Management | Pinia | 2.1 |
| HTTP Client | Axios | 1.6 |
| Build Tool | Vite | 5.0 |
| Backend Framework | FastAPI | 0.111 |
| Database | SQLite | built-in |
| Python | CPython | 3.11 |
| Deploy FE | Vercel | - |
| Deploy BE | Render | - |
