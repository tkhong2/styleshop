# Hướng dẫn Deploy

## Frontend — Vercel

### Lần đầu
```bash
cd clothing-store/frontend
npm install -g vercel
vercel
```

### Cập nhật
```bash
vercel --prod
```

### Cấu hình
- File: `vercel.json`
- Build: `npm run build`
- Output: `dist/`
- SPA rewrite: tất cả route về `index.html`

### Environment Variables (Vercel Dashboard)
| Key | Value |
|-----|-------|
| `VITE_API_BASE_URL` | `https://styleshop-8sdf.onrender.com/api` |

---

## Backend — Render

### Cấu hình service
| Setting | Value |
|---------|-------|
| Language | Python 3.11 |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |

### Environment Variables
| Key | Value |
|-----|-------|
| `ALLOWED_ORIGINS` | `https://styleshop-nine.vercel.app,http://localhost:5173` |
| `APP_NAME` | `StyleShop API` |

### Lưu ý
- Free tier spin down sau 15 phút không dùng
- Lần đầu request sau khi spin down mất ~30 giây
- Dữ liệu SQLite lưu trên disk của Render (persistent)

---

## Chạy local

### Backend
```bash
cd clothing-store/backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd clothing-store/frontend
npm install
npm run dev
```

### Expose backend ra internet (cho SePay webhook)
```bash
cloudflared tunnel --url http://localhost:8000
# Hoặc
ngrok http 8000
```

---

## SePay Webhook

Sau khi có URL public, cập nhật trong SePay:
- URL: `{PUBLIC_URL}/api/orders/webhook/sepay`
- Auth: `Apikey styleshop2026`
- Event: Có tiền vào
- TK: BIDV 8871422018
