# Nghiệp vụ: Thanh toán

## Các phương thức thanh toán

### 1. Chuyển khoản ngân hàng (BIDV + SePay)

**Luồng kỹ thuật:**
```
Frontend tạo QR ──► VietQR API
                    (img.vietqr.io/image/BIDV-{VA}-compact2.png)

User chuyển khoản ──► Tài khoản ảo VA BIDV (962471OMBS)
                      ↓
                   SePay nhận giao dịch
                      ↓
                   SePay POST webhook ──► /api/orders/webhook/sepay
                      ↓
                   Backend match mã STYLE + số tiền
                      ↓
                   Cập nhật payment_status = "paid"
                      ↓
                   Frontend polling nhận kết quả
```

**Thông tin tài khoản:**
- Ngân hàng: BIDV
- Số TK thật: 8871422018
- Số TK ảo (VA): 962471OMBS
- Chủ TK: TRAN KHAC HONG

**Webhook SePay:**
- URL: `https://styleshop-8sdf.onrender.com/api/orders/webhook/sepay`
- Auth: `Apikey styleshop2026`
- Event: Có tiền vào

### 2. Ví MoMo

Hiện tại dùng cùng QR VietQR BIDV (demo). Để tích hợp MoMo thật cần:
- Đăng ký tài khoản MoMo Business
- Dùng MoMo Payment API

### 3. COD (Thanh toán khi nhận hàng)

- Đơn hàng được tạo ngay với `payment_status: paid`
- Không cần xác nhận thêm

## Bảo mật

- API key webhook được verify qua header `Authorization: Apikey {key}`
- Chỉ xử lý giao dịch `transferType: in` (tiền vào)
- Match theo mã STYLE trong nội dung chuyển khoản
