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
            f"<tr><td style='padding:8px;border-bottom:1px solid #f0f0f0'>SP #{i['product_id']}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #f0f0f0'>{i['size']} / {i['color']}</td>"
            f"<td style='padding:8px;border-bottom:1px solid #f0f0f0;text-align:right'>x{i['quantity']}</td></tr>"
            for i in order.get("items", [])
        ])

        method_map = {"bank_transfer": "Chuyển khoản ngân hàng", "momo": "Ví MoMo", "cod": "COD"}
        payment_method = method_map.get(order.get("payment_method", ""), order.get("payment_method", ""))

        html = f"""
        <div style="font-family:Inter,Arial,sans-serif;max-width:600px;margin:0 auto;background:#fff">
          <div style="background:#1a1a1a;padding:24px;text-align:center">
            <h1 style="color:#fff;margin:0;font-size:24px;letter-spacing:2px">STYLESHOP</h1>
          </div>
          <div style="padding:32px 24px">
            <h2 style="color:#1a1a1a;margin-bottom:8px">Đặt hàng thành công! 🎉</h2>
            <p style="color:#555;margin-bottom:24px">Cảm ơn bạn đã mua sắm tại StyleShop. Đơn hàng của bạn đã được ghi nhận.</p>

            <div style="background:#f8fafc;border-radius:10px;padding:16px;margin-bottom:20px">
              <p style="margin:0 0 8px;font-size:13px;color:#888">MÃ ĐƠN HÀNG</p>
              <p style="margin:0;font-size:22px;font-weight:800;color:#1a1a1a">#{order['id']}</p>
            </div>

            <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
              <thead>
                <tr style="background:#f1f5f9">
                  <th style="padding:10px;text-align:left;font-size:12px;color:#888">SẢN PHẨM</th>
                  <th style="padding:10px;text-align:left;font-size:12px;color:#888">PHÂN LOẠI</th>
                  <th style="padding:10px;text-align:right;font-size:12px;color:#888">SL</th>
                </tr>
              </thead>
              <tbody>{items_html}</tbody>
            </table>

            <div style="border-top:2px solid #1a1a1a;padding-top:16px">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <span style="color:#555">Phương thức thanh toán</span>
                <span style="font-weight:600">{payment_method}</span>
              </div>
              <div style="display:flex;justify-content:space-between">
                <span style="font-size:16px;font-weight:700">Tổng cộng</span>
                <span style="font-size:18px;font-weight:800;color:#1a1a1a">{order['total']:,}đ</span>
              </div>
            </div>

            {"<div style='background:#fef3c7;border-radius:8px;padding:14px;margin-top:20px'><p style='margin:0;font-size:13px;color:#92400e'>⏳ Đơn hàng đang chờ thanh toán. Vui lòng chuyển khoản để hoàn tất.</p></div>" if order.get('payment_status') == 'waiting' else ""}
            {"<div style='background:#d1fae5;border-radius:8px;padding:14px;margin-top:20px'><p style='margin:0;font-size:13px;color:#065f46'>✅ Thanh toán đã được xác nhận. Chúng tôi sẽ xử lý đơn hàng sớm nhất.</p></div>" if order.get('payment_status') == 'paid' else ""}
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
