# Cơ sở dữ liệu

## Tổng quan

Dự án sử dụng **SQLite** (built-in Python) để lưu trữ đơn hàng. Dữ liệu sản phẩm hiện tại được lưu dưới dạng in-memory (file `data.py`).

## Bảng `orders`

| Cột | Kiểu | Mô tả |
|-----|------|-------|
| `id` | INTEGER PK | Mã đơn hàng tự tăng |
| `data` | TEXT (JSON) | Toàn bộ thông tin đơn hàng |

### Cấu trúc JSON trong cột `data`

```json
{
  "id": 1,
  "items": [
    {
      "product_id": 3,
      "size": "M",
      "color": "Đen",
      "quantity": 2
    }
  ],
  "total": 598000,
  "coupon": null,
  "status": "confirmed",
  "payment_method": "bank_transfer",
  "payment_status": "paid",
  "transfer_note": "STYLE123456",
  "user_id": "user@gmail.com",
  "created_at": "2026-03-30T10:00:00"
}
```

## Trạng thái đơn hàng (`status`)

| Giá trị | Mô tả |
|---------|-------|
| `pending` | Chờ xử lý |
| `confirmed` | Đã xác nhận |
| `shipping` | Đang giao hàng |
| `done` | Hoàn thành |
| `cancelled` | Đã huỷ |

## Trạng thái thanh toán (`payment_status`)

| Giá trị | Mô tả |
|---------|-------|
| `unpaid` | Chưa thanh toán |
| `waiting` | Đang chờ xác nhận |
| `paid` | Đã thanh toán |

## Phương thức thanh toán (`payment_method`)

| Giá trị | Mô tả |
|---------|-------|
| `bank_transfer` | Chuyển khoản ngân hàng (BIDV + SePay) |
| `momo` | Ví MoMo |
| `cod` | Thanh toán khi nhận hàng |
