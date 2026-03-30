# Nghiệp vụ: Xác thực người dùng

## Phương thức đăng nhập

### 1. Email + Mật khẩu
- Hiện tại dùng mock auth (chấp nhận mọi email/password)
- Token được tạo dạng `mock-token-{timestamp}`
- Lưu vào `localStorage`

### 2. Google OAuth
- Sử dụng thư viện `vue3-google-login`
- Client ID: Google Cloud Console
- Sau khi đăng nhập, decode JWT credential lấy thông tin user
- Lưu token và user vào `localStorage`

## Luồng xác thực

```
User đăng nhập
     │
     ▼
Lưu token vào localStorage
     │
     ▼
Axios interceptor tự động gắn token vào header
Authorization: Bearer {token}
     │
     ▼
Backend verify token (hiện tại chưa implement)
```

## Phân quyền

| Role | Quyền truy cập |
|------|---------------|
| Guest | Xem sản phẩm, thêm giỏ hàng |
| User | + Đặt hàng, xem lịch sử, wishlist |
| Admin | + Trang `/admin/*` |

> Hiện tại chưa có phân quyền thật — trang admin có thể truy cập tự do.
> Cần thêm route guard và role-based access control.

## Thông tin lưu trữ

```js
// localStorage
{
  "token": "mock-token-1234567890",
  "user": {
    "id": 1,
    "name": "Nguyễn Văn A",
    "email": "user@gmail.com",
    "provider": "google" // hoặc "email"
  }
}
```
