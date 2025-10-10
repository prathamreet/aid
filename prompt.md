

## 🧠 **AI Agent Prompt: Micro-Lending & Aid Distribution Web App**

**Title:** Build a “Micro-Lending and Aid Distribution” Web App using Flask + MongoDB + Tailwind

---

### 🏗️ **Project Overview**

You are an expert Python web developer.
Build a **complete web app** for a **Micro-Lending and Aid Distribution System**, where users can **register, login, request or provide financial aid**, and view a **dashboard** summarizing activity.
The app should be **simple, modern, and easily demoable** for academic presentation.

Use **Flask (Python)** for the backend, **MongoDB** for the database, and **HTML + Tailwind CSS** for the frontend (Flask templates).
No React or Next.js — keep it lightweight, but well structured.

---

### ⚙️ **Tech Stack**

* **Backend:** Flask (Python 3.10+)
* **Database:** MongoDB (use `pymongo` or `flask-pymongo`)
* **Frontend:** Jinja2 templating + TailwindCSS
* **Analytics:** Pandas + NumPy (for summary stats)
* **Chart Visualization (optional):** Chart.js or Plotly (via dashboard)

---

### 📂 **Folder Structure**

```
micro_lending_app/
│
├── app.py
├── config.py
├── requirements.txt
│
├── models/
│   └── database.py
│
├── routes/
│   ├── auth_routes.py
│   ├── aid_routes.py
│   └── dashboard_routes.py
│
├── utils/
│   └── analytics.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── request_aid.html
│
└── static/
    ├── css/
    └── js/
```

---

### 🧩 **Core Features to Implement**

#### 1. **User Authentication**

* Registration, Login, Logout (store users in MongoDB)
* Role system: `Donor`, `Beneficiary`, `Admin`
* Password hashing (use `werkzeug.security`)

#### 2. **Aid / Loan Management**

* Beneficiary can submit aid or micro-loan requests (form with name, reason, amount, category)
* Donor can view and approve/reject requests
* Store all requests in MongoDB collection `aid_requests`
* Track status: `Pending`, `Approved`, `Rejected`, `Completed`

#### 3. **Dashboard (Admin/Donor View)**

* Show total aid distributed, total donors, total beneficiaries
* Use Pandas + NumPy to generate simple analytics
* Optional chart: total aid distributed per category (Chart.js)

#### 4. **Frontend (TailwindCSS)**

* Clean modern layout using Tailwind
* Navbar with links: Home | Login | Dashboard | Request Aid | Logout
* Use base.html for templating structure (with `{% block content %}`)

#### 5. **Data Models (MongoDB Collections)**

* `users`: `{ name, email, password_hash, role }`
* `aid_requests`: `{ user_id, purpose, amount, category, status, created_at }`

#### 6. **Analytics (Optional)**

* Use Pandas to summarize:

  * Total aid amount distributed
  * Average loan size
  * Top donors/beneficiaries
  * Aid per category (Education, Health, Livelihood, etc.)

---

### 🧰 **Requirements File (example)**

```
Flask
Flask-PyMongo
pymongo
Flask-WTF
pandas
numpy
plotly
werkzeug
```

---

### 🧑‍💻 **App Flow**

1. Landing Page → explains purpose
2. Register/Login → Auth system
3. Dashboard → shows user stats & analytics
4. Request Aid → form for beneficiaries
5. Admin/Donor Dashboard → approve/reject requests
6. Logout

---

### 🧠 **Additional Notes**

* Keep UI minimal and mobile-friendly.
* Use simple Tailwind color palette.
* Add flash messages for success/failure.
* Comment code clearly (for presentation).
* Use local MongoDB (or Atlas URI via `.env`).
* Use Python 3.10+ and Flask 2.3+.

---

### 🎯 **Goal**

Create a **complete, working Flask + MongoDB app** that is **clean, functional, and presentation-ready** for a **10-minute academic project demo** — showing:

* User registration
* Aid request flow
* Dashboard with analytics

---
