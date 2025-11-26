# InvoiceGen - Professional Invoice Generator

A full-stack invoice management application built with Flask (backend) and Vue.js (frontend).

## 🚀 Features

- ✨ **User Authentication** - Secure signup and login with JWT
- 📝 **Invoice Management** - Full CRUD operations for invoices
- 👥 **Client Management** - Store and manage client details
- 📊 **Items & Calculations** - Dynamic item rows with automatic total calculations
- 💰 **Tax Calculations** - Configurable tax rates
- 📄 **PDF Generation** - Professional PDF invoices ready to download
- 🎨 **Modern UI** - Clean, responsive design with dark mode support
- 🔐 **Secure** - Protected routes and API endpoints

## 🛠️ Tech Stack

### Backend
- **Python 3.10+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **WeasyPrint** - PDF generation
- **SQLite** - Database (easily switchable to PostgreSQL)

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Vue Router** - Client-side routing
- **Pinia** - State management
- **Axios** - HTTP client
- **Bootstrap 5** - UI framework
- **Vite** - Build tool

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Node.js 18+ and npm
- pip (Python package manager)

### Backend Setup

1. **Navigate to backend directory:**
cd backend

text

2. **Create virtual environment:**
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

text

3. **Install dependencies:**
pip install -r requirements.txt

text

4. **Create `.env` file:**
cp .env.example .env

text

Edit `.env` and set your secret keys:
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

text

5. **Initialize database:**
python run.py

text
Or using Flask CLI:
flask init-db

text

6. **Run backend server:**
python run.py

text

Backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
cd frontend

text

2. **Install dependencies:**
npm install

text

3. **Run development server:**
npm run dev

text

Frontend will run on `http://localhost:5173`

## 🎯 Usage

1. **Open your browser** and navigate to `http://localhost:5173`

2. **Sign up** for a new account

3. **Login** with your credentials

4. **Create your first invoice:**
- Click "New Invoice"
- Fill in client details
- Add items with descriptions, quantities, and prices
- Set tax rate (optional)
- Add notes (optional)
- Click "Create Invoice"

5. **Manage invoices:**
- View all invoices in dashboard
- Edit existing invoices
- Change invoice status (draft, sent, paid)
- Download PDF invoices
- Delete invoices

## 📁 Project Structure

invoicegen/
├── backend/
│   ├── app.py                 # Flask app entry
│   ├── config.py              # App configuration & environment settings
│   ├── controllers.py         # All API routes (auth, invoices)
│   ├── models.py              # Database models (User, Invoice, Items)
│   ├── pdf_generator.py       # PDF creation logic
│   ├── requirements.txt       # Backend dependencies
│   ├── instance/
│   │   └── invoicegen.db      # SQLite DB (local only)
│   ├── uploads/               # Uploaded logos (local only)
│   └── .env                   # Environment variables (ignored in Git)
│
├── frontend/
│   ├── public/
│   │   ├── index.html         # Base HTML
│   │   ├── hero.png
│   │   └── accept_payment.png
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── router/            # Vue Router setup
│   │   ├── store/             # Pinia stores (auth, invoices)
│   │   ├── services/          # Axios API wrapper
│   │   ├── App.vue            # Root component
│   │   └── main.js            # Vite entrypoint
│   ├── package.json           # Frontend dependencies
│   └── vite.config.js         # Proxy & build config
│
├── .gitignore
└── README.md


## 🔑 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (protected)

### Invoices
- `GET /api/invoices` - Get all invoices (protected)
- `GET /api/invoices/:id` - Get single invoice (protected)
- `POST /api/invoices` - Create invoice (protected)
- `PUT /api/invoices/:id` - Update invoice (protected)
- `DELETE /api/invoices/:id` - Delete invoice (protected)
- `GET /api/invoices/:id/pdf` - Download PDF (protected)

## 🗄️ Database Schema

### Users
- id, email, password_hash, full_name, company_name, created_at

### Invoices
- id, invoice_number, user_id, client_name, client_email, client_address
- invoice_date, due_date, notes, subtotal, tax_rate, tax_amount, total
- status, created_at, updated_at

### Invoice Items
- id, invoice_id, description, quantity, unit_price, total

## 🚀 Deployment

### Backend (Flask)
- Use Gunicorn as WSGI server
- Deploy to Heroku, Railway, or DigitalOcean
- Switch to PostgreSQL for production
- Set environment variables securely

### Frontend (Vue)
- Build for production: `npm run build`
- Deploy to Vercel, Netlify, or Cloudflare Pages
- Update API base URL for production

## 🔒 Security Features

- Password hashing with Werkzeug
- JWT token authentication
- Protected API routes
- CORS configuration
- Input validation
- SQL injection prevention (SQLAlchemy ORM)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created for IITM Level 2 Full-Stack Project

## 🆘 Support

For issues or questions, please open an issue on GitHub.

---

**Happy Invoicing! 🎉**# starwebx_level2
