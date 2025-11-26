✨ Features
🔐 Authentication

JWT-based signup & login

Secure password hashing

Persistent sessions via token storage

🧾 Invoice Management

Create, view, update, delete invoices

Add multiple line items dynamically

Automatic subtotal, tax, discount, and total calculations

Save client details

Professional PDF generation with a clean layout

Company logo upload support

🎨 User Interface

Modern responsive UI

Dark mode support

Tailored for desktop & mobile

Smooth Vue.js experience

⚙️ Backend

RESTful API

SQLAlchemy ORM

Flask-JWT-Extended

CORS enabled for cross-origin deployments

Easy switch from SQLite → PostgreSQL

🛠️ Tech Stack
Backend

Flask

Flask-JWT-Extended

Flask-SQLAlchemy

Flask-Migrate

WeasyPrint / ReportLab (PDF)

SQLite / PostgreSQL

Frontend

Vue 3

Pinia

Vue Router

Axios

Vite

Bootstrap 5

📂 Project Structure
invoicegen/
├── backend/
│   ├── app.py                 # Flask app entry point
│   ├── config.py              # Environment & CORS configuration
│   ├── controllers.py         # API routes (Auth, Invoices)
│   ├── models.py              # ORM models
│   ├── pdf_generator.py       # Invoice PDF generator
│   ├── requirements.txt       # Python dependencies
│   ├── instance/
│   │   └── invoicegen.db      # Local SQLite database
│   ├── uploads/               # Uploaded company logos
│   └── .env                   # Backend environment variables
│
├── frontend/
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── components/        # UI components
│   │   ├── router/            # Frontend routing
│   │   ├── store/             # Pinia authentication & invoice state
│   │   ├── services/          # Axios API wrapper
│   │   ├── App.vue            # Root component
│   │   └── main.js            # Vite entry
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore

⚙️ Installation
🔧 Backend Setup
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env


Edit .env:

SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///invoicegen.db
CORS_ORIGINS=http://localhost:5173


Initialize DB:

flask init-db


Start backend:

python app.py


Backend will run at http://localhost:5000

🖥️ Frontend Setup
cd frontend
npm install
npm run dev


Frontend runs at http://localhost:5173

📄 API Endpoints
🔐 Authentication
Method	Endpoint	Description
POST	/api/auth/signup	Register new user
POST	/api/auth/login	Login user
GET	/api/auth/me	Fetch logged-in user
🧾 Invoices
Method	Endpoint	Description
GET	/api/invoices	List invoices
GET	/api/invoices/:id	Get invoice
POST	/api/invoices	Create invoice
PUT	/api/invoices/:id	Update invoice
DELETE	/api/invoices/:id	Delete invoice
GET	/api/invoices/:id/download	PDF download
🧱 Database Schema
Users
id, email, password_hash, full_name, company_name, company_logo, created_at

Invoices
id, invoice_number, user_id, client_name, client_email, client_address,
invoice_date, due_date, notes, subtotal, tax_rate, tax_amount, total,
created_at, updated_at

Invoice Items
id, invoice_id, description, quantity, unit_price, total

🚀 Deployment
▶️ Backend Deployment (Render / Railway / DigitalOcean)

Add gunicorn to requirements.txt

Render Start Command:

gunicorn 'app:app' --bind 0.0.0.0:$PORT --workers 3

Set Production Environment Variables:
FLASK_ENV=production
CORS_ORIGINS=https://your-frontend.vercel.app
SECRET_KEY=...
JWT_SECRET_KEY=...
DATABASE_URL=postgresql://...

▶️ Frontend Deployment (Vercel / Netlify)

Build:

npm run build


For Vercel, add env:

VITE_API_URL=https://your-backend.onrender.com


Then deploy.

🔒 Security Features

JWT-based protection for all API routes

Strong password hashing (Werkzeug)

Role-safe, protected endpoints

CORS protection

Server-side validation

Prevents SQL injection via SQLAlchemy ORM

📸 Screenshots

(Add your invoice UI or dashboard screenshots below)

<Place your screenshot images here>

🤝 Contributing

Pull requests are welcome!

Steps:

Fork this repo

Create a feature branch

Commit changes

Open PR 🎉

📜 License

This project is licensed under the MIT License.

👨‍💻 Author

Hanzala Tafzeel
Full-Stack Developer | IITM BS Student

🌟 Final Words

If you find this project helpful, please consider ⭐ starring the repository!

Happy Invoicing! 🧾✨