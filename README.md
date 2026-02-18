# DoughFinder

DoughFinder is a full-stack web application inspired by crowdfunding platforms.  
It allows users to create announcements, support projects through donations, and interact within a dynamic web platform.

## 🚀 Live Demo
[Live Application](https://site--doughfinder--s6d5dq7mdt7r.code.run/)

## 🧱 Tech Stack
- Python
- Flask
- PostgreSQL
- SQLAlchemy
- HTML/CSS (Jinja templates)
- Cloudinary (image management)
- Deployed on Northflank

## ✨ Features
- User registration and authentication
- Database integration with PostgreSQL
- Image upload and storage via Cloudinary
- CRUD operations
- Environment-based configuration
- Cloud deployment

## 🗄️ Database
The application uses a PostgreSQL database hosted on Northflank.  
All credentials are managed through environment variables.

## 🛠️ Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/doughfinder.git
   cd doughfinder```
   
2. Create a virtual environment:
   ```python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows```
   
3. Install dependencies:
   ```pip install -r requirements.txt```

4. Set environment variables:
   ```DATABASE_URL
   SECRET_KEY
   CLOUDINARY_URL```
   
5. Run the application:
   ```python app.py```


**Deployment**

The application is deployed on **Northflank** with a managed **PostgreSQL** database.
Sensitive data is handled through environment variables.

**Project Goal**

This project was built to strengthen backend development skills, authentication systems, database design, API integration, and cloud deployment practices.

---

# 🇮🇹 Versione Italiana

DoughFinder è una piattaforma web full-stack ispirata ai modelli di crowdfunding.
Permette agli utenti di creare annunci, supportarli tramite donazioni e interagire attraverso un'interfaccia dinamica.

## 🚀 Live Demo
[Live Application](https://site--doughfinder--s6d5dq7mdt7r.code.run/)

Il progetto è stato sviluppato per approfondire:
- sviluppo backend con Flask
- integrazione database PostgreSQL
- gestione autenticazione utenti
- integrazione servizi esterni (Cloudinary)
- deploy su piattaforma cloud
