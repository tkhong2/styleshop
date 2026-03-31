from fastapi import APIRouter, HTTPException, Request
from datetime import datetime
from typing import Optional
import time
from app.models.order import OrderCreate, Order
from app.database import load_orders, save_order, update_order, next_id
from app.email import send_order_confirmation

router = APIRouter(prefix="/orders", tags=["orders"])

# ── Tạo đơn hàng ─────────────────────────────────────────────────────────────
@router.post("", response_model=Order, status_code=201)
def create_order(payload: OrderCreate):
    order_id = next_id()
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
    save_order(order_dict)

    # Gửi email xác nhận
    if payload.user_id and "@" in payload.user_id:
        import threading
        threading.Thread(target=send_order_confirmation, args=(order_dict, payload.user_id), daemon=True).start()

    return Order(**order_dict)

# ── Polling ───────────────────────────────────────────────────────────────────
@router.get("/{order_id}/payment-status")
def get_payment_status(order_id: int):
    orders = load_orders()
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
@router.post("/webhook/sepay")
async def sepay_webhook(request: Request):
    SEPAY_API_KEY = "styleshop2026"
    payload = await request.json()
    print(f"🔔 SePay webhook: {payload}")

    auth_header = request.headers.get("Authorization", "")
    api_key = auth_header.replace("Apikey ", "").replace("apikey ", "").replace("Bearer ", "").strip()
    if api_key and api_key != SEPAY_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    transfer_type = (payload.get("transferType") or payload.get("type") or "in")
    if transfer_type.lower() == "out":
        return {"success": True, "message": "Skipped outgoing"}

    amount = payload.get("transferAmount") or payload.get("amount") or 0
    content = (payload.get("content") or payload.get("code") or "").upper()
    print(f"💰 Amount: {amount}, Content: {content}")

    matched = 0
    orders = load_orders()
    for order in orders:
        if order["payment_status"] != "waiting":
            continue
        note = (order.get("transfer_note") or "").upper()
        amount_match = int(amount) >= order["total"]
        note_match = note and note in content

        if amount_match and (note_match or True):  # fallback: match theo số tiền
            updated = update_order(order["id"], {"payment_status": "paid", "status": "confirmed"})
            if updated:
                matched += 1
                print(f"✅ Order #{order['id']} PAID!")

    return {"success": True, "matched": matched, "message": "OK"}

# ── Admin: xác nhận thủ công ──────────────────────────────────────────────────
@router.patch("/{order_id}/mark-paid")
def mark_paid(order_id: int):
    updated = update_order(order_id, {"payment_status": "paid", "status": "confirmed"})
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return {"success": True}

# ── Admin: cập nhật trạng thái đơn hàng ──────────────────────────────────────
@router.patch("/{order_id}/status")
def update_status(order_id: int, payload: dict):
    allowed = ["pending", "confirmed", "shipping", "done", "cancelled"]
    new_status = payload.get("status")
    if new_status not in allowed:
        raise HTTPException(status_code=400, detail=f"Status phải là: {allowed}")
    updated = update_order(order_id, {"status": new_status})
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return {"success": True, "status": new_status}
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    return {"success": True}

# ── Lịch sử đơn hàng ─────────────────────────────────────────────────────────
@router.get("/me", response_model=list[Order])
def get_my_orders(user_id: Optional[str] = None):
    orders = load_orders()
    if user_id:
        orders = [o for o in orders if o.get("user_id") == user_id]
    return [Order(**o) for o in reversed(orders)]
