# API Endpoints

Base URL: `https://styleshop-8sdf.onrender.com/api`

Swagger UI: `https://styleshop-8sdf.onrender.com/docs`

---

## Products

### GET /products
Lấy danh sách sản phẩm.

**Query params:**
| Param | Type | Mô tả |
|-------|------|-------|
| `category` | string | `ao`, `quan`, `vay`, `giay`, `tui` |
| `gender` | string | `nam`, `nu`, `unisex` |
| `is_sale` | boolean | Lọc hàng sale |
| `is_new` | boolean | Lọc hàng mới |
| `q` | string | Tìm kiếm theo tên/mô tả |
| `skip` | int | Bỏ qua N sản phẩm (phân trang) |
| `limit` | int | Số sản phẩm trả về (max 200) |

**Response:**
```json
[
  {
    "id": 1,
    "name": "Áo Thun Basic Cotton Trắng",
    "price": 299000,
    "original_price": 299000,
    "category": "ao",
    "gender": "unisex",
    "image": "https://...",
    "images": ["https://..."],
    "sizes": ["S", "M", "L", "XL"],
    "colors": ["Trắng", "Đen", "Xám"],
    "description": "...",
    "rating": 4.5,
    "reviews": 312,
    "is_new": false,
    "is_sale": false
  }
]
```

### GET /products/:id
Lấy chi tiết một sản phẩm.

---

## Orders

### POST /orders
Tạo đơn hàng mới.

**Request body:**
```json
{
  "items": [
    { "product_id": 1, "size": "M", "color": "Đen", "quantity": 2 }
  ],
  "total": 598000,
  "coupon": "STYLE10",
  "payment_method": "bank_transfer",
  "user_id": "user@gmail.com"
}
```

**Response:** Order object với `transfer_note` (mã chuyển khoản)

### GET /orders/me
Lấy đơn hàng của user.

**Query params:** `user_id` (email)

### GET /orders/:id/payment-status
Kiểm tra trạng thái thanh toán (dùng cho polling).

**Response:**
```json
{
  "order_id": 1,
  "payment_status": "waiting",
  "status": "pending",
  "total": 598000,
  "transfer_note": "STYLE123456"
}
```

### POST /orders/webhook/sepay
Nhận webhook từ SePay khi có giao dịch.

**Headers:** `Authorization: Apikey styleshop2026`

### PATCH /orders/:id/mark-paid
Xác nhận thanh toán thủ công (admin).

---

## Categories

### GET /categories
```json
[
  { "id": "ao", "name": "Áo" },
  { "id": "quan", "name": "Quần" },
  { "id": "vay", "name": "Váy & Đầm" }
]
```
