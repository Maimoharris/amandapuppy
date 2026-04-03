# Pawsome Pets E-Commerce Platform

A professional, full-featured Django e-commerce website for dog breeding and pet accessories marketplace with Tailwind CSS.

## Features

### Core Features
- ✅ **Dog Breeding Marketplace** - Browse and purchase dogs/puppies by breed category
- ✅ **Pet Accessories Store** - Full e-commerce for pet products
- ✅ **Advanced Filtering** - Filter dogs and accessories by multiple criteria
- ✅ **Product Ratings & Reviews** - User ratings for both dogs and accessories
- ✅ **Wishlist System** - Save favorite items for later
- ✅ **Shopping Cart** - Full cart functionality with session management
- ✅ **Adoption Process** - Comprehensive adoption form before checkout
- ✅ **Multiple Product Images** - Upload multiple images per product
- ✅ **"Sold" Badge Display** - Automatic "SOLD" overlay on sold dogs
- ✅ **User Authentication** - Register, login, and track orders
- ✅ **Guest Checkout** - Purchase without account (adoption still possible)

### Advanced Features
- ✅ **Post Ad Section** - Users can post their own pet-related ads
- ✅ **Payment Contact Popup** - Contact information modal at checkout
- ✅ **Social Media Integration** - Share buttons and social links
- ✅ **Partner Display** - Showcase trusted pet vendor partners
- ✅ **Hero Video Section** - Video hero on homepage
- ✅ **Favorite Breeds Section** - Featured breed categories
- ✅ **Search Functionality** - Search dogs and accessories
- ✅ **Newsletter Subscription** - Email collection for marketing
- ✅ **Contact Form** - Professional contact page
- ✅ **About Us Page** - Dynamic about page from admin
- ✅ **Tawk.to Chat Integration** - Live chat widget
- ✅ **Order Management** - User order history and tracking
- ✅ **Responsive Design** - Mobile-first, fully responsive

### Admin Features
- ✅ **Site Settings Management** - Control all site content from admin
- ✅ **Dynamic Social Media Links** - Edit social media URLs from admin
- ✅ **Payment Gateway Display** - Toggle payment icons
- ✅ **Content Management** - Rich text editor for descriptions
- ✅ **Order Management** - Track and update orders
- ✅ **Ad Approval System** - Review and approve user-posted ads
- ✅ **Adoption Application Review** - Review adoption requests

## Technology Stack

- **Backend:** Django 5.0.1
- **Frontend:** Tailwind CSS 3.x (CDN)
- **Database:** SQLite (easily switchable to PostgreSQL/MySQL)
- **Rich Text:** CKEditor
- **Icons:** Font Awesome 6.5
- **Fonts:** Google Fonts (Inter, Poppins)

## Color Palette (Professional Design)

- **Primary:** Warm terracotta (#cd4735 - #e06451)
- **Secondary:** Sky blue (#0ba5e9 - #0369a1)
- **Accent:** Gold/Yellow (#facc15 - #ca8a04)
- **Neutral:** Stone grays (#fafaf9 - #1c1917)

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip

### Step 1: Install Dependencies

```bash
cd pawsome_pets
pip install -r requirements.txt
```

### Step 2: Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Step 4: Create Initial Site Settings

After running migrations, log into the admin panel and create a SiteSettings instance:

```bash
python manage.py runserver
```

Navigate to `http://127.0.0.1:8000/admin/` and:
1. Login with your superuser credentials
2. Go to "Site Settings" and click "Add"
3. Fill in all the required information
4. Save

### Step 5: Add Sample Data (Optional)

You can manually add:
- Breed categories (e.g., Labrador, German Shepherd, Poodle)
- Accessory categories (e.g., Car Seats, Carpets, Toys, Food Bowls)
- Dogs with multiple images
- Accessories with multiple images
- Partners (pet vendors)
- Hero videos

## Configuration

### Tawk.to Chat Widget Setup

1. Sign up at [Tawk.to](https://www.tawk.to/)
2. Get your Property ID and Widget ID
3. Add them in Django Admin → Site Settings

### Email Configuration

For production, update `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### Payment Gateway Integration

The current setup shows a contact popup for payment. To integrate real payment gateways:

1. **Stripe:** Use `dj-stripe` package
2. **PayPal:** Use `django-paypal` package
3. **Square:** Use Square API

Update the checkout view to process actual payments.

## Usage

### Admin Panel

Access: `http://127.0.0.1:8000/admin/`

#### Adding Dogs:
1. Go to "Dogs" → "Add Dog"
2. Fill in all dog information
3. Save and add images via "Dog Images"
4. Set one image as primary

#### Managing Orders:
1. View all orders in "Orders"
2. Update order status
3. Mark payment as confirmed
4. View adoption forms linked to orders

#### Site Settings:
- Update contact information
- Change social media links
- Edit About Us content
- Configure chat widget

### Frontend URLs

- Homepage: `/`
- Dogs: `/dogs/`
- Accessories: `/accessories/`
- Cart: `/cart/`
- Wishlist: `/wishlist/` (requires login)
- Post Ad: `/post-ad/` (requires login)
- About: `/about/`
- Contact: `/contact/`

## Key Features Explanation

### 1. Adoption Flow
When a customer wants to adopt a dog:
1. Browse dogs
2. Click "Adopt"
3. Fill adoption application form
4. Proceed to checkout
5. Complete shipping/billing info
6. Contact popup appears for payment arrangement

### 2. "Sold" Badge
When a dog is marked as sold in admin:
- Red "SOLD" badge automatically appears on dog image
- Dog still visible but cannot be added to cart
- Remove from featured listings automatically

### 3. Product Ratings
Users can rate and review:
- Each dog breed
- Each accessory
- Star ratings (1-5)
- Written reviews

### 4. Wishlist
Logged-in users can:
- Add dogs to wishlist
- Add accessories to wishlist
- View all wishlist items
- Remove items

### 5. Post Ad Section
Users can post:
- Selling ads
- Adoption offers
- Pet services
- Lost/Found pets

Admins review and approve before public display.

## File Structure

```
pawsome_pets/
├── pawsome_pets_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/
│   ├── models.py (15+ models)
│   ├── views.py (40+ views)
│   ├── forms.py (8 forms)
│   ├── admin.py (comprehensive admin)
│   ├── urls.py
│   └── context_processors.py
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── dogs/ (4 templates)
│   ├── accessories/ (4 templates)
│   ├── cart/ (1 template)
│   ├── wishlist/ (1 template)
│   ├── auth/ (3 templates)
│   ├── checkout/ (3 templates)
│   ├── adoption/ (1 template)
│   ├── account/ (2 templates)
│   └── post_ad/ (4 templates)
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
│   ├── dogs/
│   ├── accessories/
│   └── hero_videos/
├── requirements.txt
└── README.md
```

## Customization

### Changing Colors

Edit `templates/base.html` and modify the Tailwind config:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: { ... },
                secondary: { ... },
                // Change colors here
            }
        }
    }
}
```

### Adding New Features

The codebase is modular and easy to extend:
- Add models in `core/models.py`
- Create views in `core/views.py`
- Add URLs in `core/urls.py`
- Create templates in `templates/`

## Deployment

### Production Checklist

1. **Security:**
   - Change `SECRET_KEY` in settings.py
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`

2. **Database:**
   - Switch to PostgreSQL or MySQL
   - Run migrations

3. **Static Files:**
   ```bash
   python manage.py collectstatic
   ```

4. **Media Files:**
   - Configure cloud storage (AWS S3, Cloudinary)
   - Or serve via web server (Nginx)

5. **Web Server:**
   - Use Gunicorn + Nginx
   - Or deploy to platforms like:
     - Heroku
     - DigitalOcean
     - AWS
     - PythonAnywhere

## Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Tailwind CSS docs: https://tailwindcss.com/docs

## License

This project is provided as-is for commercial use.

## Credits

- Font Awesome for icons
- Google Fonts for typography
- Tailwind CSS for styling
- Django framework

---

**Built with ❤️ for Pawsome Pets**
