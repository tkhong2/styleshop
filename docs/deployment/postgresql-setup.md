# Setup PostgreSQL trên Render + Email với Resend

## 1. Tạo PostgreSQL database trên Render

1. Vào [render.com](https://render.com) → **New** → **PostgreSQL**
2. Điền:
   - Name: `styleshop-db`
   - Database: `styleshop`
   - User: `styleshop`
   - Region: Singapore
   - Plan: **Free**
3. Click **Create Database**
4. Sau khi tạo xong, copy **Internal Database URL** (dạng `postgresql://...`)

## 2. Thêm DATABASE_URL vào Render Web Service

1. Vào Web Service `styleshop-api` → **Environment**
2. Thêm biến:
   - Key: `DATABASE_URL`
   - Value: paste URL từ bước trên
3. Save → Render tự redeploy

## 3. Setup Email với Resend (miễn phí 3000 email/tháng)

1. Đăng ký tại [resend.com](https://resend.com)
2. Vào **API Keys** → **Create API Key** → copy key
3. Thêm vào Render Environment:
   - `RESEND_API_KEY` = `re_xxxxxxxxxxxx`
   - `FROM_EMAIL` = `StyleShop <noreply@yourdomain.com>`

> Lưu ý: Resend free tier chỉ gửi được đến email đã verify.
> Để gửi đến bất kỳ email nào, cần verify domain tại Resend → Domains.

## 4. Verify domain (tùy chọn)

Nếu có domain riêng:
1. Resend → **Domains** → **Add Domain**
2. Thêm DNS records theo hướng dẫn
3. Sau khi verify, đổi `FROM_EMAIL` thành `noreply@yourdomain.com`
