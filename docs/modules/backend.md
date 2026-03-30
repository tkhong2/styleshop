# Module Backend

## Cấu trúc thư mục

```
backend/
├── app/
│   ├── main.py          # FastAPI app, CORS, routers
│   ├── database.py      # SQLite helpers
│   ├── data.py          # 100 sản phẩm mẫu
│   ├── models/
│   │   ├── product.py   # Pydantic model Product
│   │   └── order.py     # Pydantic models Order, OrderCreate
│   └── routers/
│       ├── products.py  # GET /api/products, /api/products/:id
│       ├── orders.py    # POST/GET /api/orders, webhook
│       └── categories.py # GET /api/categories
├── requirements.txt
├── .env
├── .python-version      # Python 3.11
└── render.yaml          # Render deploy config
```

## Routers

### Products (`/api/products`)

| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/api/products` | Lấy danh sách sản phẩm (có filter) |
| GET | `/api/products/:id` | Lấy chi tiết sản phẩm |

Query params: `category`, `gender`, `is_sale`, `is_new`, `q` (tìm kiếm), `skip`, `limit`

### Orders (`/api/orders`)

| Method | Path | Mô tả |
|--------|------|-------|
| POST | `/api/orders` | Tạo đơn hàng mới |
| GET | `/api/orders/me` | Lấy đơn hàng của user |
| GET | `/api/orders/:id/payment-status` | Kiểm tra trạng thái thanh toán |
| POST | `/api/orders/webhook/sepay` | Nhận webhook từ SePay |
| PATCH | `/api/orders/:id/mark-paid` | Xác nhận thanh toán thủ công |

### Categories (`/api/categories`)

| Method | Path | Mô tả |
|--------|------|-------|
| GET | `/api/categories` | Lấy danh sách danh mục |

## Middleware

- **CORS**: Cho phép request từ frontend (Vercel + localhost)
- **Uvicorn**: ASGI server

## Environment Variables

| Key | Mô tả |
|-----|-------|
| `APP_NAME` | Tên ứng dụng |
| `ALLOWED_ORIGINS` | Danh sách domain được phép CORS |
| `DB_PATH` | Đường dẫn file SQLite |
