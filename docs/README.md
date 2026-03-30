# StyleShop - Tài liệu dự án

## Tổng quan

StyleShop là website thương mại điện tử bán quần áo, được xây dựng với:

- **Frontend**: Vue 3 + Pinia + Vue Router + Vite
- **Backend**: FastAPI (Python) + SQLite
- **Deploy**: Vercel (frontend) + Render (backend)
- **Thanh toán**: BIDV + SePay webhook (VietQR)
- **Xác thực**: Email/Password (mock) + Google OAuth (GIS)

## Links

- Frontend: https://styleshop-nine.vercel.app
- Backend API: https://styleshop-8sdf.onrender.com
- API Docs: https://styleshop-8sdf.onrender.com/docs
- Admin: https://styleshop-nine.vercel.app/admin

## Cấu trúc tài liệu

| Thư mục | Nội dung |
|---------|----------|
| `architecture/` | Kiến trúc hệ thống, database schema |
| `modules/` | Mô tả chi tiết frontend & backend |
| `business/` | Nghiệp vụ đặt hàng, thanh toán, xác thực |
| `api/` | Tài liệu API endpoints |
| `deployment/` | Hướng dẫn deploy |
| `features/` | Danh sách tính năng đã triển khai |
