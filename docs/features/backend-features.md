# Tính năng Backend

## API Endpoints

### Products
| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/api/products` | Lấy danh sách (filter: category, gender, is_sale, is_new, q, skip, limit) |
| GET | `/api/products/:id` | Chi tiết sản phẩm |

### Orders
| Method | Path | Mô tả |
|--------|------|-------|
| POST | `/api/orders` | Tạo đơn hàng |
| GET | `/api/orders/me` | Đơn hàng theo user_id |
| GET | `/api/orders/:id/payment-status` | Polling trạng thái thanh toán |
| POST | `/api/orders/webhook/sepay` | Nhận webhook từ SePay |
| PATCH | `/api/orders/:id/mark-paid` | Xác nhận thủ công (admin) |

### Categories
| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/api/categories` | Danh sách danh mục |

## Database (SQLite)

File: `orders.db` — persistent trên Render

```sql
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  data TEXT NOT NULL  -- JSON
)
```

### Cấu trúc JSON đơn hàng
```json
{
  "id": 1,
  "items": [{"product_id": 1, "size": "M", "color": "Đen", "quantity": 2}],
  "total": 598000,
  "coupon": "STYLE10",
  "status": "confirmed",
  "payment_method": "bank_transfer",
  "payment_status": "paid",
  "transfer_note": "STYLE123456",
  "user_id": "user@gmail.com",
  "shipping": {"name": "...", "phone": "...", "address": "..."},
  "created_at": "2026-03-30T10:00:00"
}
```

## Thanh toán SePay + BIDV

### Luồng
```
User chuyển khoản vào VA BIDV (962471OMBS)
  → SePay nhận giao dịch
  → POST /api/orders/webhook/sepay
  → Backend match số tiền + mã STYLE
  → Cập nhật payment_status = "paid"
  → Frontend polling nhận kết quả
```

### Cấu hình
- Ngân hàng: BIDV
- Số TK thật: 8871422018
- Số TK ảo (VA): 962471OMBS
- Webhook URL: `https://styleshop-8sdf.onrender.com/api/orders/webhook/sepay`
- Auth: `Apikey styleshop2026`

## Dữ liệu sản phẩm

100 sản phẩm trong `app/data.py`:
- Áo: 38 sản phẩm (thun, sơ mi, khoác, hoodie, blazer, len, crop, polo...)
- Quần: 18 sản phẩm (jeans, short, tây, jogger, legging, culottes...)
- Váy & Đầm: 22 sản phẩm (hoa, maxi, mini, midi, đầm liền, jumpsuit...)
- Giày: 12 sản phẩm (sneaker, cao gót, sandal, búp bê, boot, loafer...)
- Túi: 10 sản phẩm (tote, bucket, đeo chéo, clutch, balo, ví...)

## Mã giảm giá (frontend)
| Mã | Giảm |
|----|------|
| STYLE10 | 10% |
| SALE20 | 20% |
| NEWUSER | 15% |
