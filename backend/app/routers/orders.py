from fastapi import APIRouter, HTTPException, Header, Request
from datetime import datetime
from typing import Optional
import json, os, time
from app.models.order import OrderCreate, Order

router = APIRouter(prefix="/orders", tags=["orders"])

# ── Persistent storage dùng file JSON (thay thế in-memory) ───────────────────
DB_FILE = "orders_db.json"

def _load() -> list[dict]:
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save(orders: list[dict]):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, default=str)

def _next_id() -> int:
    orders = _load()
    return max((o["id"] for o in orders), default=0) + 1

# ── Tạo đơn hàng ─────────────────────────────────────────────────────────────
@router.post("", response_model=Order, status_code=201)
def create_order(payload: OrderCreate):
    order_id = _next_id()
    transfer_note = f"STYLE{int(time.time()) % 1000000:06d}"
    payment_status = "paid" if payload.payment_method == "cod" else "waiting"
    status = "confirmed" if payload.payment_method == "cod" else "pending"

    order_dict = {
        "id": order_id,
        "items": [i.model_dump() for i in payload.items],
        "total": payload.total,
        "coupon": payload.coupon,
        "status": status,
        "payment_method": payload.payment_method or "cod",
        "payment_status": payment_status,
        "transfer_note": transfer_note,
        "user_id": payload.user_id,
        "created_at": datetime.utcnow().isoformat(),
    }
    orders = _load()
    orders.append(order_dict)
    _save(orders)
    return Order(**order_dict)

# ── Polling ───────────────────────────────────────────────────────────────────
@router.get("/{order_id}/payment-status")
def get_payment_status(order_id: int):
    orders = _load()
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return {
        "order_id": order["id"],
        "payment_status": order["payment_status"],
        "status": order["status"],
        "total": order["total"],
        "transfer_note": order["transfer_note"],
    }

# ── SePay Webhook ─────────────────────────────────────────────────────────────
# SePay gửi POST khi có giao dịch vào tài khoản BIDV
# Docs: https://my.sepay.vn/userapi/docs
#
# Payload mẫu từ SePay:
# {
#   "id": 12345,
#   "gateway": "BIDV",
#   "transactionDate": "2026-03-29 10:00:00",
#   "accountNumber": "8871422018",
#   "subAccount": null,
#   "code": "STYLE123456",          ← nội dung chuyển khoản
#   "content": "STYLE123456 thanh toan don hang",
#   "transferType": "in",           ← "in" = tiền vào
#   "transferAmount": 500000,
#   "accumulated": 1000000,
#   "referenceCode": "FT26088...",
#   "description": "...",
#   "apiKey": "your_sepay_api_key"  ← SePay gửi kèm để verify
# }
@router.post("/webhook/sepay")
async def sepay_webhook(request: Request):
    SEPAY_API_KEY = "styleshop2026"

    payload = await request.json()

    # Log toàn bộ payload để debug
    print(f"🔔 SePay webhook received: {payload}")
    print(f"🔔 Headers: {dict(request.headers)}")

    auth_header = request.headers.get("Authorization", "")
    # SePay gửi: "Authorization": "Apikey YOUR_KEY" (chữ A hoa)
    api_key = auth_header.replace("Apikey ", "").replace("apikey ", "").replace("Bearer ", "").strip()
    print(f"🔑 Auth header: '{auth_header}', extracted key: '{api_key}'")
    if api_key and api_key != SEPAY_API_KEY:
        print(f"❌ Invalid API key: '{api_key}' vs expected '{SEPAY_API_KEY}'")
        raise HTTPException(status_code=401, detail="Invalid API key")

    # SePay dùng nhiều field khác nhau tùy version
    transfer_type = (
        payload.get("transferType") or
        payload.get("transfer_type") or
        payload.get("type") or "in"
    )

    # Bỏ qua giao dịch tiền ra
    if transfer_type.lower() == "out":
        return {"success": True, "message": "Skipped outgoing"}

    amount = (
        payload.get("transferAmount") or
        payload.get("transfer_amount") or
        payload.get("amount") or 0
    )

    content = (
        payload.get("content") or
        payload.get("code") or
        payload.get("description") or
        payload.get("memo") or ""
    ).upper()

    print(f"💰 Amount: {amount}, Content: {content}")

    matched = 0
    orders = _load()
    for order in orders:
        if order["payment_status"] != "waiting":
            continue
        note = (order.get("transfer_note") or "").upper()
        content_upper = content.upper()
        print(f"🔍 Checking order #{order['id']}: note={note}, total={order['total']}, content={content_upper}")

        # Match nếu nội dung chứa mã đơn HOẶC số tiền khớp
        note_match = note and note in content_upper
        amount_match = int(amount) >= order["total"]

        if amount_match and (note_match or not content_upper.strip()):
            # Khớp nếu số tiền đúng VÀ (có mã khớp HOẶC nội dung trống)
            order["payment_status"] = "paid"
            order["status"] = "confirmed"
            matched += 1
            print(f"✅ Order #{order['id']} PAID! Amount={amount}, note_match={note_match}")
        elif amount_match and not note_match:
            # Fallback: số tiền khớp nhưng không có mã → vẫn xác nhận
            order["payment_status"] = "paid"
            order["status"] = "confirmed"
            matched += 1
            print(f"✅ Order #{order['id']} PAID via amount fallback! Amount={amount}")

    _save(orders)

    print(f"✅ Webhook processed, matched={matched}")
    # SePay yêu cầu response có "success": true để xác nhận webhook thành công
    return {"success": True, "matched": matched, "message": "OK"}

# ── Admin: xác nhận thanh toán thủ công ──────────────────────────────────────
@router.patch("/{order_id}/mark-paid")
def mark_paid(order_id: int):
    orders = _load()
    order = next((o for o in orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    order["payment_status"] = "paid"
    order["status"] = "confirmed"
    _save(orders)
    return {"success": True}

# ── Lịch sử đơn hàng theo user ───────────────────────────────────────────────
@router.get("/me", response_model=list[Order])
def get_my_orders(user_id: Optional[str] = None):
    orders = _load()
    if user_id:
        orders = [o for o in orders if o.get("user_id") == user_id]
    return [Order(**o) for o in reversed(orders)]
