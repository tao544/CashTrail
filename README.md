# 💰 Cashtrail

> A smart financial management platform that helps parents monitor their children's spending while empowering kids to build responsible money habits with confidence.

![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google OAuth](https://img.shields.io/badge/Google_OAuth-2.0-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

---

## 📖 About

Cashtrail bridges the gap between parental oversight and children's financial independence. Parents manage the family's financial ecosystem — creating accounts for their children, funding wallets, and monitoring spending habits from a dedicated dashboard. Children log in with their provided credentials and independently track their own expenses, building financial awareness from an early age.

---

## ✨ Features

### For Parents
- 🔐 **Google OAuth Login** — secure, one-click sign-in via Google
- 👨‍👧 **Child Account Management** — create accounts for children with username and password credentials
- 🔑 **Password Reset** — reset a child's password directly from the parent dashboard
- 💳 **Wallet Funding** — fund each child's wallet to control their spending power
- 📊 **Spending Overview** — monitor each child's expense habits from the parent dashboard

### For Children
- 🔐 **Credential-based Login** — log in with parent-provided username and password
- 💸 **Expense Tracking** — log and manage daily expenses
- 📈 **Personal Dashboard** — visualize spending patterns through charts
- 🧾 **Transaction History** — view a detailed record of all past transactions

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6 |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Django Allauth + Google OAuth 2.0 |
| Database | PostgreSQL |
| Static Files | WhiteNoise |
| Deployment | Render |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip
- Git
- A Google Cloud project with OAuth 2.0 credentials

### Installation

```bash
# Clone the repository
git clone https://github.com/tao554/cashtrail.git
cd cashtrail

# Create and activate a virtual environment
python -m venv .expensetracker
source .expensetracker/bin/activate  # Windows: .expensetracker\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Run the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## ⚙️ Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services → Credentials**
4. Create an **OAuth 2.0 Client ID** (Web application)
5. Add to **Authorized redirect URIs**:
   ```
   http://127.0.0.1:8000/accounts/google/login/callback/
   ```
6. In Django Admin → **Sites** → update the domain to match your environment
7. In Django Admin → **Social Applications** → add your Google Client ID and Secret

---

## 🗂️ Project Structure

```
Cashtrail/
├── Cashtrail/          # Project settings and URLs
├── main/               # Core app (models, views, templates)
├── templates/          # HTML templates
├── static/             # CSS, JS, images
├── staticfiles/        # Collected static files (production)
├── manage.py
└── requirements.txt
```

---

## 🔮 Future Enhancements

- [ ] **Payment Integration** — fund children's wallets via Paystack or Flutterwave
- [ ] **Spending Limits** — parents set monthly or weekly caps per child
- [ ] **Expense Categories** — detailed categorization and filtering of expenses
- [ ] **Reports & Exports** — download spending reports as PDF or CSV
- [ ] **Notifications** — alerts when a child approaches their spending limit

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Taoheed Adepoju**  
📧 adepojutaoheed23@gmail.com

---

> *"Financial literacy starts at home."* 🏠
