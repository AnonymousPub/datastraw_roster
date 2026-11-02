# DataStraw Smart Roster Management System

A robust, enterprise-grade, browser-based employee scheduling and operational rostering application built for automated shift management, leave tracking, and multi-brand coverage validation.

---

## 🚀 Key Features

* **Automated Scheduling Engine**: Generates monthly operational rosters while respecting weekly offs, public holidays, and approved employee leaves.
* **Coverage Validation & Conflict Detection**: Automatically checks daily staffing against brand-specific minimum requirements and logs `CoverageIssues` upon shortages.
* **Role & Resource Management**: Manage employees, organizational pods, client brands (e.g., *Brand Apex, Brand Nexus, Brand Zenith*), and customer/technical processes (*CS, ACC, NDR*).
* **Operations Command Dashboard**: Real-time high-level metrics summary tracking active staff, operational pods, client brands, generated rosters, and recent conflict warnings.
* **Admin Control Panel**: Full Django admin integration for fine-tuned data management.

---

## 🛠️ Tech Stack & Architecture

* **Backend**: Python 3.12, Django 4.2 LTS (chosen for robust relational ORM and MariaDB/MySQL compatibility)
* **Database**: MySQL (XAMPP local environment)
* **Frontend**: Bootstrap 5, Responsive HTML5/CSS3 templates
* **Testing**: Pytest & Pytest-Django validation suites
* **Pattern**: MVT (Model-View-Template)

---

## ⚙️ Installation & Local Setup

1. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   
   Install Dependencies:

Bash
pip install -r requirements.txt
Configure Database:
Ensure XAMPP MySQL is running on port 3306, and create a database named datastraw_roster_db.

Run Migrations & Seed Data:

Bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
Run the Development Server:

Bash
python manage.py runserver
Access the app in your browser at http://127.0.0.1:8000/.

🧪 Running Automated Tests
To run the test suite with pytest-django:

Bash
pytest --ds=datastraw_project.settings
📄 Project Structure
datastraw_project/ - Django core configuration, settings, and root URLs.

roster/ - Core application module containing models, views, templates, and pytest test suites.

requirements.txt - Python project dependency package specifications.