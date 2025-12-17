# 🚀 XBlog — Django Blog System
## Personal Blog Web

---

## 🏆 News
- [Dec.17] Base version released

---

## 📋 Project Overview

XBlog is a Django-based personal blog system providing a complete blogging workflow, including user accounts, post management, categories and search, Markdown rendering, and rich interaction features (like, favorite, comment, reply, comment-like).

The project is designed for **course experiments and personal blog starters**, emphasizing **clean structure, correctness, and extensibility**.

---

## ✨ Core Innovations

- **Bio-first subtitle**: homepage subtitle prioritizes user bio (fallback if empty)
- **Clean post summary**: render Markdown first, then strip code blocks / inline code
- **Avatar UX refinement**: fixed display size, default fallback, delete confirmation, empty-file protection
- **Category & search integration**: auto-create/associate category; homepage supports keyword search (title/content/author/category)
- **Idempotent interactions**: like / favorite / comment-like as toggle actions
- **Unified layout & theme**: Bootswatch theme, sticky footer, reserved homepage logo

---

## ⚙️ Installation & Run

### 1️⃣ Install Dependencies

▶ Recommended (Tsinghua mirror)
```bash
pip install -i https://pypi.tsinghua.edu.cn/simple django pillow python-dotenv markdown
```
▶ Or (default source)
```bash
pip install django pillow python-dotenv markdown
```
Or install via requirements.txt:
```bash
pip install -r requirements.txt
```

### 2️⃣ Initialize & Run
```bash
# Enter project root (where manage.py is located)
cd XBlog

# Initialize database
python manage.py makemigrations
python manage.py migrate

# Create admin account (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

---

## 🌐 Quick Navigation

- Homepage (list/search/pagination): /
- Post detail: /<slug>/
- Create post: /create/
- Edit post: /<slug>/edit/
- Profile: /me/
- My Favorites: /favorites/
- Auth: /accounts/signup / /accounts/login / /accounts/logout

---

## 📁 Project Structure
```bash
XBlog/
├── .git/                        # Git repository
├── blog/                        # Blog application (App)
│   ├── __init__.py
│   ├── admin.py                 # Admin registrations
│   ├── apps.py
│   ├── forms.py                 # Post / Avatar / Profile / Comment forms
│   ├── models.py                # Profile / Category / Post / Like / Favorite / Comment
│   ├── urls.py                  # App-level routing
│   ├── views.py                 # Business logic
│   ├── tests.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0005_profile_bio.py  # Bio field extension
│   └── templates/
│       └── blog/
│           ├── index.html       # Homepage
│           ├── post_detail.html # Post detail & interactions
│           └── profile.html     # Profile & avatar management
│
├── mysite/                      # Django project (Settings)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # i18n / timezone / media / CSRF
│   ├── urls.py                  # Project-level routing
│   └── wsgi.py
│
├── manage.py                    # Django entry point
├── db.sqlite3                   # SQLite database
├── requirements.txt             # Dependencies
├── .env.example                 # Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🌟 Feature Summary
- Like / Favorite / “My Favorites”
- Comment / Reply / Comment Like
- Category & keyword search
- Markdown + code highlight
- Profile avatar & bio
- Sticky footer & themed UI
- CSRF protection & permission checks
- Asia/Shanghai timezone & Chinese localization

---

## ✨ Contact

Auy issues, feel free to contact.

Email: 2024150065@mails.szu.edu.cn
