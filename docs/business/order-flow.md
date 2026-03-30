# Nghiệp vụ: Quy trình đặt hàng

## Sơ đồ luồng

```
[Khách hàng]
     │
     ▼
[Duyệt sản phẩm] ──► [Trang chủ / Danh sách / Chi tiết]
     │
     ▼
[Thêm vào giỏ hàng] ──► Lưu localStorage (Pinia cart store)
     │
     ▼
[Xem giỏ hàng] ──► Kiểm tra số lượng, cập nhật, xoá
     │
     ▼
[Chọn phương thức thanh toán]
     │
     ├──► COD ──────────────────────────────────────────────────────┐
     │                                                               │
     ├──► Chuyển khoản ngân hàng (BIDV + VietQR)                   │
     │         │                                                     │
     │         ▼                                                     │
     │    [Tạo đơn hàng] ──► POST /api/orders                      │
     │         │              (status: pending, payment: waiting)   │
     │         ▼                                                     │
     │    [Hiển thị QR + thông tin chuyển khoản]                   │
     │         │                                                     │
     │         ▼                                                     │
     │    [User chuyển khoản vào VA BIDV]                          │
     │         │                                                     │
     │         ▼                                                     │
     │    [SePay nhận giao dịch]                                   │
     │         │                                                     │
     │         ▼                                                     │
     │    [SePay gửi webhook] ──► POST /api/orders/webhook/sepay   │
     │         │                                                     │
     │         ▼                                                     │
     │    [Backend cập nhật] ──► payment_status: paid              │
     │         │                                                     │
     │         ▼                                                     │
     │    [Frontend polling] ──► GET /api/orders/:id/payment-status │
     │         │                                                     │
     └─────────┴─────────────────────────────────────────────────────┘
                                    │
                                    ▼
                          [Hiển thị đặt hàng thành công]
                                    │
                                    ▼
                          [Xoá giỏ hàng]
```

## Quy tắc nghiệp vụ

### Giỏ hàng
- Lưu trữ ở localStorage, không cần đăng nhập
- Mỗi item được phân biệt bởi `(product_id, size, color)`
- Số lượng tối thiểu: 1

### Phí vận chuyển
- Đơn hàng < 500.000đ: phí 30.000đ (test: 1.000đ)
- Đơn hàng ≥ 500.000đ: miễn phí

### Mã giảm giá
| Mã | Giảm |
|----|------|
| `STYLE10` | 10% |
| `SALE20` | 20% |
| `NEWUSER` | 15% |

### Xác nhận thanh toán
- Polling mỗi 5 giây, tối đa 5 phút
- Nếu webhook nhận được và số tiền >= tổng đơn → tự động xác nhận
- Admin có thể xác nhận thủ công qua trang `/admin/orders`
