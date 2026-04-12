"""
Email service dùng Resend (https://resend.com) — miễn phí 3000 email/tháng.
Cần set RESEND_API_KEY trong env.
"""
import os
from typing import Optional

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "StyleShop <noreply@styleshop.vn>")


def send_order_confirmation(order: dict, to_email: Optional[str] = None):
    """Gửi email xác nhận đơn hàng."""
    if not RESEND_API_KEY or not to_email:
        print(f"📧 [Email skipped] No API key or email. Order #{order['id']}")
        return

    try:
        import resend
        resend.api_key = RESEND_API_KEY

        items_html = "".join([
            f"""<tr>
              <td style='padding:10px 8px;border-bottom:1px solid #f0f0f0;font-size:14px'>
                {i.get('name') or f"Sản phẩm #{i['product_id']}"}
              </td>
              <td style='padding:10px 8px;border-bottom:1px solid #f0f0f0;font-size:13px;color:#666'>
                {i['size']} / {i['color']}
              </td>
              <td style='padding:10px 8px;border-bottom:1px solid #f0f0f0;text-align:center;font-size:13px'>
                x{i['quantity']}
              </td>
              <td style='padding:10px 8px;border-bottom:1px solid #f0f0f0;text-align:right;font-size:14px;font-weight:600'>
                {f"{i['price'] * i['quantity']:,}đ" if i.get('price') else ''}
              </td>
            </tr>"""
            for i in order.get("items", [])
        ])

        method_map = {"bank_transfer": "Chuyển khoản ngân hàng", "momo": "Ví MoMo", "cod": "COD (Thanh toán khi nhận hàng)", "qr": "Chuyển khoản ngân hàng"}
        payment_method = method_map.get(order.get("payment_method", ""), order.get("payment_method", ""))

        # Thông tin giao hàng
        shipping = order.get("shipping") or {}
        shipping_html = ""
        if shipping.get("name"):
            addr_parts = [shipping.get("address", ""), shipping.get("district", ""), shipping.get("city", "")]
            full_addr = ", ".join(p for p in addr_parts if p)
            shipping_html = f"""
            <div style="background:#f8fafc;border-radius:10px;padding:16px;margin-bottom:20px">
              <p style="margin:0 0 10px;font-size:12px;font-weight:700;color:#888;letter-spacing:1px">THÔNG TIN GIAO HÀNG</p>
              <p style="margin:0 0 4px;font-size:14px;font-weight:600">{shipping['name']}</p>
              <p style="margin:0 0 4px;font-size:13px;color:#555">{shipping.get('phone', '')}</p>
              <p style="margin:0;font-size:13px;color:#555">{full_addr}</p>
              {f"<p style='margin:4px 0 0;font-size:12px;color:#888;font-style:italic'>Ghi chú: {shipping['note']}</p>" if shipping.get('note') else ''}
            </div>"""

        payment_note_html = ""
        if order.get("payment_status") == "waiting":
            payment_note_html = f"""
            <div style='background:#fef3c7;border-radius:8px;padding:14px;margin-top:20px'>
              <p style='margin:0 0 6px;font-size:13px;font-weight:700;color:#92400e'>⏳ Chờ thanh toán</p>
              <p style='margin:0;font-size:13px;color:#92400e'>Vui lòng chuyển khoản với nội dung: <strong>{order.get('transfer_note', '')}</strong></p>
            </div>"""
        elif order.get("payment_status") == "paid":
            payment_note_html = """
            <div style='background:#d1fae5;border-radius:8px;padding:14px;margin-top:20px'>
              <p style='margin:0;font-size:13px;color:#065f46'>✅ Thanh toán đã được xác nhận. Chúng tôi sẽ xử lý đơn hàng sớm nhất.</p>
            </div>"""

        html = f"""
        <div style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;background:#fff">
          <div style="background:#1a1a1a;padding:24px;text-align:center">
            <h1 style="color:#fff;margin:0;font-size:24px;letter-spacing:2px">STYLESHOP</h1>
          </div>
          <div style="padding:32px 24px">
            <h2 style="color:#1a1a1a;margin-bottom:8px">Đặt hàng thành công! 🎉</h2>
            <p style="color:#555;margin-bottom:24px">Cảm ơn bạn đã mua sắm tại StyleShop. Đơn hàng của bạn đã được ghi nhận.</p>

            <div style="background:#f8fafc;border-radius:10px;padding:16px;margin-bottom:20px">
              <p style="margin:0 0 4px;font-size:12px;font-weight:700;color:#888;letter-spacing:1px">MÃ ĐƠN HÀNG</p>
              <p style="margin:0;font-size:26px;font-weight:800;color:#1a1a1a">#{order['id']}</p>
            </div>

            {shipping_html}

            <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
              <thead>
                <tr style="background:#f1f5f9">
                  <th style="padding:10px 8px;text-align:left;font-size:12px;color:#888;font-weight:600">SẢN PHẨM</th>
                  <th style="padding:10px 8px;text-align:left;font-size:12px;color:#888;font-weight:600">PHÂN LOẠI</th>
                  <th style="padding:10px 8px;text-align:center;font-size:12px;color:#888;font-weight:600">SL</th>
                  <th style="padding:10px 8px;text-align:right;font-size:12px;color:#888;font-weight:600">THÀNH TIỀN</th>
                </tr>
              </thead>
              <tbody>{items_html}</tbody>
            </table>

            <div style="border-top:2px solid #1a1a1a;padding-top:16px">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="color:#555;font-size:14px">Phương thức thanh toán</span>
                <span style="font-weight:600;font-size:14px">{payment_method}</span>
              </div>
              <div style="display:flex;justify-content:space-between">
                <span style="font-size:16px;font-weight:700">Tổng cộng</span>
                <span style="font-size:20px;font-weight:800;color:#1a1a1a">{order['total']:,}đ</span>
              </div>
            </div>

            {payment_note_html}
          </div>
          <div style="background:#f8fafc;padding:20px;text-align:center;border-top:1px solid #e2e8f0">
            <p style="margin:0;font-size:12px;color:#888">Hotline: 1800 1162 | Email: cskh@styleshop.vn</p>
            <p style="margin:4px 0 0;font-size:12px;color:#aaa">© 2026 StyleShop. All rights reserved.</p>
          </div>
        </div>
        """

        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [to_email],
            "subject": f"StyleShop — Xác nhận đơn hàng #{order['id']}",
            "html": html,
        })
        print(f"✅ Email sent to {to_email} for order #{order['id']}")

    except Exception as e:
        print(f"❌ Email error: {e}")


ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")

def send_admin_notification(order: dict):
    """Gửi email thông báo đơn hàng mới đến admin."""
    if not RESEND_API_KEY or not ADMIN_EMAIL:
        print(f"📧 [Admin notify skipped] No API key or admin email. Order #{order['id']}")
        return

    try:
        import resend
        resend.api_key = RESEND_API_KEY

        method_map = {"bank_transfer": "Chuyển khoản", "momo": "MoMo", "cod": "COD", "qr": "Chuyển khoản QR"}
        payment_method = method_map.get(order.get("payment_method", ""), order.get("payment_method", ""))

        shipping = order.get("shipping") or {}
        shipping_info = ""
        if shipping.get("name"):
            addr_parts = [shipping.get("address", ""), shipping.get("district", ""), shipping.get("city", "")]
            full_addr = ", ".join(p for p in addr_parts if p)
            shipping_info = f"{shipping['name']} · {shipping.get('phone', '')} · {full_addr}"
        else:
            shipping_info = order.get("user_id", "Chưa có")

        items_text = "".join([
            f"<li style='margin-bottom:4px'>{i.get('name') or f'SP #{i[\"product_id\"]}'} — {i['size']}/{i['color']} x{i['quantity']}</li>"
            for i in order.get("items", [])
        ])

        html = f"""
        <div style="font-family:Inter,Arial,sans-serif;max-width:560px;margin:0 auto;background:#fff;border:1px solid #e2e8f0;border-radius:12px;overflow:hidden">
          <div style="background:#1e293b;padding:16px 24px;display:flex;align-items:center;gap:12px">
            <div style="background:#3b82f6;width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:16px">🛍️</div>
            <div>
              <p style="margin:0;color:#fff;font-size:15px;font-weight:700">StyleShop Admin</p>
              <p style="margin:0;color:#94a3b8;font-size:12px">Thông báo đơn hàng mới</p>
            </div>
          </div>
          <div style="padding:24px">
            <p style="margin:0 0 16px;font-size:15px;color:#1e293b">Có đơn hàng mới vừa được đặt:</p>

            <table style="width:100%;border-collapse:collapse;margin-bottom:16px">
              <tr>
                <td style="padding:8px 0;font-size:13px;color:#64748b;width:140px">Mã đơn hàng</td>
                <td style="padding:8px 0;font-size:14px;font-weight:700;color:#3b82f6">#{order['id']}</td>
              </tr>
              <tr style="background:#f8fafc">
                <td style="padding:8px;font-size:13px;color:#64748b">Khách hàng</td>
                <td style="padding:8px;font-size:13px">{order.get('user_id') or 'Khách vãng lai'}</td>
              </tr>
              <tr>
                <td style="padding:8px 0;font-size:13px;color:#64748b">Giao đến</td>
                <td style="padding:8px 0;font-size:13px">{shipping_info}</td>
              </tr>
              <tr style="background:#f8fafc">
                <td style="padding:8px;font-size:13px;color:#64748b">Thanh toán</td>
                <td style="padding:8px;font-size:13px;font-weight:600">{payment_method}</td>
              </tr>
              <tr>
                <td style="padding:8px 0;font-size:13px;color:#64748b">Tổng tiền</td>
                <td style="padding:8px 0;font-size:16px;font-weight:800;color:#1e293b">{order['total']:,}đ</td>
              </tr>
            </table>

            <div style="background:#f8fafc;border-radius:8px;padding:14px;margin-bottom:16px">
              <p style="margin:0 0 8px;font-size:12px;font-weight:700;color:#64748b">SẢN PHẨM</p>
              <ul style="margin:0;padding-left:16px;font-size:13px;color:#334155">{items_text}</ul>
            </div>

            <a href="https://styleshop-nine.vercel.app/admin/orders"
              style="display:inline-block;background:#3b82f6;color:#fff;padding:10px 20px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none">
              Xem đơn hàng →
            </a>
          </div>
          <div style="background:#f8fafc;padding:12px 24px;border-top:1px solid #e2e8f0;font-size:11px;color:#94a3b8;text-align:center">
            Đây là email tự động từ hệ thống StyleShop. Vui lòng không trả lời email này.
          </div>
        </div>
        """

        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [ADMIN_EMAIL],
            "subject": f"[StyleShop] Đơn hàng mới #{order['id']} — {order['total']:,}đ ({payment_method})",
            "html": html,
        })
        print(f"✅ Admin notified for order #{order['id']}")

    except Exception as e:
        print(f"❌ Admin notify error: {e}")
