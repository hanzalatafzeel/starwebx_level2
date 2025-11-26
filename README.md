# 🚀 InvoiceGen – Professional Invoice Generator

![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/invoicegen?color=blue)
![GitHub stars](https://img.shields.io/github/stars/yourusername/invoicegen?style=social)
![Maintenance](https://img.shields.io/badge/Maintained-yes-brightgreen)
![License MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A full-stack **Invoice Management Application** built with **Flask (Backend)** and **Vue.js (Frontend)**.  
Create, manage, and download beautiful invoices with your business branding.

---

## ✨ Features

### 🔐 Authentication
- JWT-based signup & login  
- Secure password hashing  
- Auto-persist login session  

### 🧾 Invoice Management
- Create, edit, delete invoices  
- Unlimited line items  
- Automatic totals and tax calculations  
- Manage client details  
- Auto-generate invoice numbers  
- PDF invoice download  
- Upload company logo  

### 🎨 Modern UI
- Responsive dashboard  
- Clean layout (mobile-friendly)  
- Dark-mode compatible  

### ⚙️ Backend Highlights
- REST API with Flask  
- SQLAlchemy ORM  
- JWT Authentication  
- PDF Generation (ReportLab / WeasyPrint)  
- CORS Enabled  

---

## 🛠 Tech Stack

### Backend
- Flask  
- SQLAlchemy  
- Flask-Migrate  
- Flask-JWT-Extended  
- ReportLab / WeasyPrint  
- SQLite / PostgreSQL  

### Frontend
- Vue 3  
- Pinia  
- Vue Router  
- Axios  
- Bootstrap 5  
- Vite  

---

## 📂 Project Structure

```
invoicegen/
├── backend/
│   ├── app.py                 # Flask application entry
│   ├── config.py              # Environment & CORS config
│   ├── controllers.py         # All API routes
│   ├── models.py              # Database models
│   ├── pdf_generator.py       # PDF creation logic
│   ├── requirements.txt
│   ├── instance/
│   │   └── invoicegen.db
│   ├── uploads/               # Uploaded logo files
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── router/
│   │   ├── store/
│   │   ├── services/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## ⚙️ Installation

### 🔧 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///invoicegen.db
CORS_ORIGINS=http://localhost:5173
```

Initialize database:

```bash
flask init-db
```

Run backend:

```bash
python app.py
```

### 🖥️ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: `http://localhost:5173`

---

## 📄 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register |
| POST | `/api/auth/login` | Login |
| GET | `/api/auth/me` | Get current user |

### Invoices

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/invoices` | List invoices |
| GET | `/api/invoices/:id` | Get invoice |
| POST | `/api/invoices` | Create invoice |
| PUT | `/api/invoices/:id` | Update invoice |
| DELETE | `/api/invoices/:id` | Delete invoice |
| GET | `/api/invoices/:id/download` | Download PDF |

---

## 🗄 Database Schema

### Users
- `id`, `email`, `password_hash`, `full_name`, `company_name`, `company_logo`, `created_at`

### Invoices
- `id`, `invoice_number`, `user_id`, `client_name`, `client_email`, `client_address`, `invoice_date`, `due_date`, `notes`, `subtotal`, `tax_rate`, `tax_amount`, `total`, `created_at`, `updated_at`

### Invoice Items
- `id`, `invoice_id`, `description`, `quantity`, `unit_price`, `total`

---

## 🚀 Deployment

### Backend (Render / Railway)

Install gunicorn:

```bash
pip install gunicorn
```

Render Start Command:

```bash
gunicorn 'app:app' --bind 0.0.0.0:$PORT --workers 3
```

Environment Variables:

```env
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
SECRET_KEY=xxxx
JWT_SECRET_KEY=xxxx
DATABASE_URL=postgresql://...
```

### Frontend (Vercel / Netlify)

Set environment variable:

```env
VITE_API_URL=https://your-backend.onrender.com
```

Build:

```bash
npm run build
```

Deploy the `dist/` folder.

---

## 🔒 Security

- JWT tokens
- Password hashing
- CORS protection
- ORM SQL injection prevention
- Sanitized API inputs

---

## 🤝 Contributing

1. Fork the repo
2. Create a new branch
3. Commit your changes
4. Submit a Pull Request

---

## 📜 License

MIT License

---

## 👨‍💻 Author

**Hanzala Tafzeel**  
Full-Stack Developer | IITM BS Data Science Student

---

## ⭐ Support

If you liked this project, please give it a star ⭐ on GitHub!