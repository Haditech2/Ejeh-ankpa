# Ejeh Ankpa Palace Platform

A production-ready Django web platform for the traditional institution of the Ejeh of Ankpa, preserving cultural heritage and connecting the community.

## Features

- **5 User Roles**: Ejeh, Palace Administrators, Council of Chiefs, Community Members, Public Visitors
- **Ejeh Profiles**: Present and past Ejehs with detailed biographies
- **Royal Gallery**: Categorized photo gallery with lightbox
- **Announcements**: Royal messages and palace news
- **Events Calendar**: Ceremonies, festivals, and community events
- **Community Engagement**: Contact forms, feedback, newsletter
- **Responsive Design**: Bootstrap 5 with AOS animations

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL
- **Media Storage**: Cloudinary
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Animations**: AOS (Animate On Scroll)
- **Static Files**: WhiteNoise
- **Deployment**: Vercel

## Installation

### Prerequisites

- Python 3.11+
- PostgreSQL
- Cloudinary account

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ejeh
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   copy .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Seed initial data (Optional but Recommended)**
   ```bash
   # Seed Ejeh profile and historical events
   python manage.py seed_data
   
   # Or seed with admin user
   python manage.py seed_data --admin
   ```

7. **Create superuser (if not using --admin flag)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

9. **Run development server**
   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000`

## Data Seeding

The platform includes a data seeding command that populates the database with the current Ejeh's biography (HRH Alhaji Abubakar Sadiq Ahmed Yakubu, Ejeh Ankpa IV) and historical events.

```bash
# Seed Ejeh profile and historical events
python manage.py seed_data

# Seed with default admin user (admin@ejehankpa.com / admin123)
python manage.py seed_data --admin
```

Alternatively, you can load the fixture directly:
```bash
python manage.py loaddata palace/fixtures/ejeh_data.json
```

## Project Structure

```
ejeh/
├── ejeh_palace/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/             # User authentication & profiles
├── palace/               # Core palace content
├── announcements/        # News & royal messages
├── events/               # Events & ceremonies
├── community/            # Contact & feedback
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── requirements.txt
├── vercel.json          # Vercel deployment config
└── manage.py
```

## User Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| Ejeh | Traditional ruler | Full access |
| Palace Admin | Palace staff | Manage content |
| Chief | Council member | View & moderate |
| Member | Registered community | Basic access |
| Visitor | Public | Read-only |

## Deployment to Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. Set environment variables in Vercel dashboard:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `CLOUDINARY_CLOUD_NAME`
   - `CLOUDINARY_API_KEY`
   - `CLOUDINARY_API_SECRET`
   - `DEBUG=False`

## Admin Panel

Access the Django admin at `/admin/` to:
- Manage users and roles
- Add/edit Ejeh profiles
- Upload gallery images
- Create announcements and events
- View contact messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary to Ejeh Ankpa Palace.

## Support

For support, contact the palace administration or submit an issue.

---

*Preserving the heritage of Ankpa Kingdom for generations to come.*
