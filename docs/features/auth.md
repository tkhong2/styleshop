# Xác thực & Phân quyền

## Phương thức đăng nhập

### 1. Email + Mật khẩu (Mock)
- Chấp nhận mọi email/password (chưa có backend auth thật)
- Token: `mock-token-{timestamp}`
- Lưu vào localStorage

### 2. Google OAuth (Google Identity Services)
- Client ID: `532996264964-8tfficegp4q2tdavi84c5119cl3jgid0.apps.googleusercontent.com`
- Dùng `window.google.accounts.oauth2.initTokenClient`
- Lấy user info từ `https://www.googleapis.com/oauth2/v3/userinfo`
- Script GIS load trong `index.html`

## Phân quyền

| Role | Email | Quyền |
|------|-------|-------|
| Admin | `khachong2102005@gmail.com` | Truy cập `/admin/*` |
| User | Bất kỳ | Truy cập trang người dùng |
| Guest | Chưa đăng nhập | Xem sản phẩm, thêm giỏ hàng |

## Route Guard

```js
// router/index.js
beforeEnter: (to, from, next) => {
  const auth = useAuthStore()
  const ADMIN_EMAILS = ['khachong2102005@gmail.com']
  if (!auth.isLoggedIn) next('/login?redirect=' + to.fullPath)
  else if (!ADMIN_EMAILS.includes(auth.user?.email)) next('/')
  else next()
}
```

## Redirect sau đăng nhập
- Email admin → `/admin`
- User thường → `/` hoặc `?redirect=` param
- Google OAuth → tương tự

## Thêm admin mới
Thêm email vào 2 chỗ:
1. `src/router/index.js` — mảng `ADMIN_EMAILS`
2. `src/views/Login.vue` — mảng `ADMIN_EMAILS`
