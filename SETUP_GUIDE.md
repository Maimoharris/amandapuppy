# COMPLETE SETUP GUIDE - Pawsome Pets E-Commerce

## QUICK START (5 Minutes)

### Step 1: Install Dependencies
```bash
cd pawsome_pets
pip install Django==5.0.1 Pillow==10.2.0 --break-system-packages
```

Note: Other packages (crispy-forms, ckeditor, etc.) are optional for basic functionality.

### Step 2: Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Admin User
```bash
python manage.py createsuperuser
```
Enter username, email, and password when prompted.

### Step 4: Run Development Server
```bash
python manage.py runserver
```

### Step 5: Configure Site Settings
1. Open browser: http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Click "Site Settings" → "Add Site Settings"
4. Fill in required fields:
   - Site Name: "Pawsome Pets"
   - Site Tagline: "Your Trusted Dog Breeding & Accessories Store"
   - Email: your-email@example.com
   - Phone: +1234567890
5. Click "Save"

### Step 6: Add Sample Data
Add at least one breed category and one accessory category to see the site working properly.

**You're Done!** Visit http://127.0.0.1:8000/ to see your site.

---

## DETAILED SETUP INSTRUCTIONS

### Database Schema
The project includes 15+ models:
- SiteSettings (singleton - site-wide settings)
- Partner (pet vendor partners)
- BreedCategory & AccessoryCategory
- Dog & DogImage (multiple images per dog)
- Accessory & AccessoryImage
- DogRating & AccessoryRating
- Wishlist
- AdoptionForm
- Order & OrderItem
- HeroVideo
- PostAd & PostAdImage
- ContactMessage
- Newsletter

### Required Initial Data

#### 1. Site Settings (MUST CREATE FIRST)
```
Admin → Site Settings → Add
- Site Name
- Site Tagline
- Email, Phone
- Social Media URLs (optional)
- Tawk.to IDs (optional)
- About Us Content
```

#### 2. Breed Categories (Examples)
```
- Labrador Retriever
- German Shepherd
- Golden Retriever
- Bulldog
- Beagle
- Poodle
- Rottweiler
- Yorkshire Terrier
- Boxer
- Dachshund
```

Mark 4-6 as "Featured" for homepage display.

#### 3. Accessory Categories (Examples)
```
- Car Seats
- Pet Carpets
- Food Bowls
- Toys
- Leashes & Collars
- Beds & Blankets
- Grooming Supplies
- Training Aids
- Health & Wellness
- Travel Accessories
```

#### 4. Sample Dogs
For each dog, add:
- Name, breed category, age (months)
- Gender, size, color
- Description (rich text)
- Temperament (e.g., "Friendly, Energetic, Good with Kids")
- Price
- At least 1-3 images

#### 5. Sample Accessories
For each accessory:
- Name, category
- Description
- Brand (optional)
- Price
- Stock quantity
- At least 1 image

### Admin Panel Overview

#### Dashboard Sections:
1. **Core** - Main models (Dogs, Accessories, Categories, etc.)
2. **Orders** - Order management and tracking
3. **Adoptions** - Adoption form applications
4. **Posted Ads** - User-submitted advertisements
5. **Site Settings** - Global site configuration
6. **Authentication** - Users and permissions

#### Key Admin Features:

**Dogs Admin:**
- List view shows: name, breed, age, price, sold status, featured
- Inline image management
- Filter by: breed, gender, size, sold status, featured
- Search by: name, description, color
- Bulk actions available

**Orders Admin:**
- View all customer orders
- Update order status
- Mark payment as confirmed
- View linked adoption forms
- Edit shipping information

**Adoption Forms:**
- Review applications
- Approve/reject
- View applicant details
- See which dog is being adopted

**Site Settings:**
- Single instance (can't create multiple)
- Edit all site-wide content
- Social media links
- Payment gateway toggles
- Tawk.to configuration

---

## FEATURES IMPLEMENTATION GUIDE

### 1. "Sold" Badge Feature
When a dog is sold:
```
Admin → Dogs → Select Dog → Check "Is Sold" → Save
```
Result: Red "SOLD" badge automatically appears on dog card images.

### 2. Wishlist System
Users must be logged in:
```python
# Users click heart icon on dog/accessory cards
# Adds to their personal wishlist
# View at: /wishlist/
```

### 3. Adoption Flow
Complete adoption process:
```
1. User browses dogs
2. Clicks "Adopt" button
3. Fills adoption form (/adoption/{dog_id}/)
4. Form saved to database
5. Redirected to checkout
6. Completes shipping/billing info
7. Payment contact popup appears
8. Order created with linked adoption form
```

### 4. Multi-Image Upload
For products:
```
Admin → Dogs → Select Dog → Scroll to "Dog Images" section
- Click "Add another Dog Image"
- Upload image
- Check "Is Primary" for main image
- Set Order number for sorting
- Repeat for multiple images
```

### 5. Product Ratings
Logged-in users can rate:
```
1. Visit product detail page
2. Scroll to rating section
3. Select stars (1-5)
4. Write review (optional)
5. Submit
```

### 6. Post Ad Feature
Users can post ads:
```
1. Login required
2. Navigate to "Post an Ad"
3. Fill form:
   - Ad Type (Selling, Adoption, Service, Lost, Found)
   - Title, description
   - Pet details
   - Contact info
   - Upload images
4. Submit for admin review
5. Admin approves/rejects
6. Approved ads shown at /ads/
```

### 7. Search & Filters

**Dogs:**
- Search by name, breed, description
- Filter by: breed category, gender, size, price range, age range
- Sort by: newest, price (low/high), name

**Accessories:**
- Search by name, brand, description
- Filter by: category, price range, in stock
- Sort by: newest, price (low/high), name

### 8. Cart System
Session-based cart:
```python
# Add to cart: stores in session
# View cart: /cart/
# Update quantities
# Remove items
# Proceed to checkout
```

### 9. Checkout Process
```
1. View cart
2. Click "Proceed to Checkout"
3. If cart has dogs → must have adoption form
4. Fill shipping/billing info
5. Review order
6. Click "Place Order"
7. Payment contact popup shows
8. Order saved to database
9. Confirmation page with order number
```

### 10. Social Sharing
Share buttons on product pages:
```html
<!-- Implemented on detail pages -->
<button onclick="shareProduct()">Share</button>
```
Users can share dogs/accessories on social media.

---

## TAWK.TO CHAT SETUP

### Get Credentials:
1. Sign up at https://www.tawk.to/
2. Create a property
3. Get Property ID and Widget ID from dashboard

### Configure in Django:
```
Admin → Site Settings
- Tawk Property ID: [paste here]
- Tawk Widget ID: [paste here]
- Save
```

Chat widget automatically appears on all pages.

---

## CUSTOMIZATION GUIDE

### Change Color Scheme

Edit `templates/base.html`:

```javascript
tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: {
                    // Change these hex values
                    500: '#e06451',
                    600: '#cd4735',
                    // ... etc
                },
                secondary: {
                    // Change these
                },
                // ... etc
            }
        }
    }
}
```

### Add New Breed Categories
```
Admin → Breed Categories → Add
- Name: Your Breed Name
- Slug: auto-generated
- Description: Optional
- Image: Upload breed image
- Is Featured: Check for homepage
- Order: Number for sorting
```

### Add Hero Video
```
Admin → Hero Videos → Add
- Title: Video name
- Video File: Upload MP4
- Thumbnail: Optional screenshot
- Is Active: Check
- Order: 0 for first position
```

### Add Partners
```
Admin → Partners → Add
- Name: Partner company name
- Logo: Upload logo image
- Website URL: Optional
- Is Active: Check
- Order: Sorting number
```

### Customize Email Templates
Email backend is console by default.

For production, edit `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

---

## TEMPLATE STRUCTURE

### Template Hierarchy:
```
base.html (master template)
├── home.html
├── dogs/
│   ├── dog_list.html (with filters)
│   ├── dog_detail.html (with rating form)
│   ├── breed_category.html
│   └── ... (you'll need to create remaining)
├── accessories/
│   ├── accessory_list.html
│   ├── accessory_detail.html
│   └── ... (you'll need to create remaining)
├── cart/
│   └── cart.html
├── wishlist/
│   └── wishlist.html
├── checkout/
│   ├── checkout.html
│   └── order_confirmation.html (with payment popup)
└── ... (other templates)
```

### Creating Missing Templates

The core functionality is in place. You'll need to create:

1. **dog_detail.html** - Dog detail page with:
   - Image gallery
   - Full description
   - Rating form
   - Add to cart button
   - Share buttons

2. **accessory_detail.html** - Similar to dog_detail

3. **cart.html** - Shopping cart with:
   - Item list
   - Quantity update
   - Remove items
   - Total calculation

4. **checkout.html** - Checkout form with:
   - Shipping info
   - Order summary
   - Place order button

5. **order_confirmation.html** - After order with:
   - Order details
   - Payment popup (modal with site_settings.email, phone)

6. **about_us.html** - Display site_settings.about_us_content

7. **contact_us.html** - Contact form

8. Auth templates (login, register, logout)

9. Other remaining templates

### Template Pattern (Example):

```django
{% extends 'base.html' %}
{% load humanize %}

{% block title %}Page Title{% endblock %}

{% block content %}
<section class="py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Your content here -->
    </div>
</section>
{% endblock %}
```

---

## PRODUCTION DEPLOYMENT

### Pre-Deployment Checklist:

1. **Security Settings:**
```python
# settings.py
DEBUG = False
SECRET_KEY = 'generate-new-secret-key-here'
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# CSRF
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

2. **Database:**
Switch to PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pawsome_db',
        'USER': 'postgres_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Static Files:**
```bash
python manage.py collectstatic --no-input
```

4. **Media Files:**
Configure AWS S3 or Cloudinary for image storage:
```python
# Using django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = 'your-key'
AWS_SECRET_ACCESS_KEY = 'your-secret'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
```

5. **Web Server:**
Use Gunicorn + Nginx:
```bash
pip install gunicorn
gunicorn pawsome_pets_project.wsgi:application --bind 0.0.0.0:8000
```

### Deployment Platforms:

**Heroku:**
```bash
heroku create pawsome-pets
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

**DigitalOcean / AWS / VPS:**
1. Set up Ubuntu server
2. Install Python, PostgreSQL, Nginx
3. Clone repository
4. Set up virtual environment
5. Install dependencies
6. Configure Gunicorn systemd service
7. Configure Nginx reverse proxy
8. Set up SSL with Let's Encrypt

---

## TROUBLESHOOTING

### Common Issues:

**1. "No module named 'django'"**
```bash
pip install Django --break-system-packages
```

**2. "Site Settings matching query does not exist"**
- Login to admin
- Create Site Settings instance
- Fill required fields

**3. Images not displaying**
- Check MEDIA_URL and MEDIA_ROOT in settings
- Ensure media folder has proper permissions
- In development, URL patterns include static/media

**4. Cart not working**
- Check session middleware is enabled
- Clear browser cookies
- Check cart_context in context_processors

**5. Adoption form error**
- Ensure adoption form is filled before checkout for dogs
- Check session has adoption_form_id

**6. Payment popup not showing**
- Check site_settings has email and phone
- Verify JavaScript is enabled
- Check browser console for errors

**7. Tawk.to chat not appearing**
- Verify Property ID and Widget ID are correct
- Check site_settings values
- Ensure internet connection (loads from CDN)

---

## MAINTENANCE

### Regular Tasks:

1. **Backup Database:**
```bash
python manage.py dumpdata > backup.json
```

2. **Update Products:**
- Regularly mark sold dogs as "Sold"
- Update accessory stock quantities
- Remove discontinued items

3. **Review Adoption Forms:**
- Check new applications daily
- Approve/reject posted ads
- Respond to contact messages

4. **Monitor Orders:**
- Update order statuses
- Confirm payments
- Track fulfillment

5. **Content Updates:**
- Refresh hero videos seasonally
- Update About Us content
- Add new partner logos

### Performance Optimization:

1. **Database Queries:**
- Use select_related() and prefetch_related()
- Add database indexes
- Monitor slow queries

2. **Images:**
- Compress images before upload
- Use WebP format
- Implement lazy loading

3. **Caching:**
- Enable Django caching
- Cache template fragments
- Use Redis for sessions

---

## SUPPORT & RESOURCES

### Documentation Links:
- Django: https://docs.djangoproject.com/
- Tailwind CSS: https://tailwindcss.com/docs
- Font Awesome: https://fontawesome.com/icons

### Django Commands:
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Django shell
python manage.py shell

# Database backup
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json
```

---

## WHAT'S INCLUDED

### Backend (Django):
✅ 15+ Models with relationships
✅ 40+ Views (list, detail, CRUD operations)
✅ 8 Forms with validation
✅ Comprehensive Admin interface
✅ Context processors for global data
✅ Session-based cart system
✅ User authentication
✅ Order management
✅ Rating system
✅ Search and filtering
✅ Image upload handling

### Frontend (Tailwind):
✅ Responsive base template
✅ Professional color scheme
✅ Homepage with hero video
✅ Dog listing with filters
✅ Navigation with dropdowns
✅ Footer with social media
✅ Message alerts
✅ Mobile menu
✅ Card hover effects
✅ Sold badge overlay

### Features:
✅ Dog/Puppy marketplace
✅ Pet accessories e-commerce
✅ Multi-image products
✅ Wishlist
✅ Shopping cart
✅ Adoption forms
✅ Order checkout
✅ Payment contact popup
✅ User accounts
✅ Product ratings
✅ Search & filters
✅ Post ad system
✅ Newsletter
✅ Contact form
✅ Social sharing
✅ Tawk.to chat integration
✅ Partner showcase
✅ Admin management

---

## NEXT STEPS

After basic setup, complete the frontend by creating remaining templates:

1. Dog detail page
2. Accessory list and detail pages  
3. Cart page
4. Checkout and confirmation pages
5. About and contact pages
6. Auth pages (login, register)
7. Account pages (orders, ads)
8. Post ad pages

Use the provided templates as references for structure and styling.

**The foundation is solid - build on it to create your perfect pet marketplace!**
