from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField
import os


class SiteSettings(models.Model):
    """Site-wide settings manageable from admin"""
    site_name = models.CharField(max_length=200, default="Pawsome Pets")
    site_tagline = models.CharField(max_length=300, default="Your Trusted Dog Breeding & Accessories Store")
    site_description = models.TextField(blank=True)
    
    # Contact Information
    email = models.EmailField(default="info@pawsomepets.com")
    phone = PhoneNumberField(default="+1234567890")
    whatsapp = PhoneNumberField(blank=True, null=True)
    address = models.TextField(blank=True)
    
    # Social Media Links
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    pinterest_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    
    # Business Hours
    business_hours = models.TextField(default="Mon-Fri: 9AM-6PM, Sat: 10AM-4PM, Sun: Closed")
    
    # Tawk.to Chat Widget
    tawk_property_id = models.CharField(max_length=100, blank=True, help_text="Tawk.to Property ID")
    tawk_widget_id = models.CharField(max_length=100, blank=True, help_text="Tawk.to Widget ID")
    
    # About Us Content
    about_us_content = RichTextField(blank=True)
    about_us_image = models.ImageField(upload_to='site_images/', blank=True, null=True)
    
    # Footer Content
    footer_text = models.TextField(blank=True, default="© 2024 Pawsome Pets. All rights reserved.")
    
    # Payment Methods Display
    show_visa = models.BooleanField(default=True)
    show_mastercard = models.BooleanField(default=True)
    show_paypal = models.BooleanField(default=True)
    show_amex = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Only one Site Settings instance is allowed')
        return super().save(*args, **kwargs)


class Partner(models.Model):
    """Pet vendor partners"""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/')
    website_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class BreedCategory(models.Model):
    """Dog breed categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='breed_categories/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage as favorite breed")
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Breed Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class AccessoryCategory(models.Model):
    """Accessory categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='accessory_categories/', blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Accessory Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Dog(models.Model):
    """Dog/Puppy listings"""
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    
    SIZE_CHOICES = [
        ('small', 'Small (0-25 lbs)'),
        ('medium', 'Medium (26-60 lbs)'),
        ('large', 'Large (61-100 lbs)'),
        ('giant', 'Giant (100+ lbs)'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    breed_category = models.ForeignKey(BreedCategory, on_delete=models.CASCADE, related_name='dogs')
    
    # Basic Information
    age_months = models.IntegerField(help_text="Age in months")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    color = models.CharField(max_length=100)
    
    # Details
    description = RichTextField()
    temperament = models.CharField(max_length=300, help_text="e.g., Friendly, Energetic, Calm")
    health_status = models.CharField(max_length=300, default="Vaccinated and Healthy")
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_negotiable = models.BooleanField(default=False)
    
    # Status
    is_sold = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_available_for_adoption = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.breed_category.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.breed_category.name}")
            slug = base_slug
            counter = 1
            while Dog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum([r.rating for r in ratings]) / len(ratings)
        return 0
    
    def rating_count(self):
        return self.ratings.count()


class DogImage(models.Model):
    """Multiple images for dogs"""
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='dogs/')
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    alt_text = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-is_primary', 'order']
    
    def __str__(self):
        return f"Image for {self.dog.name}"
    
    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary images
        if self.is_primary:
            DogImage.objects.filter(dog=self.dog, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class Accessory(models.Model):
    """Pet accessories"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(AccessoryCategory, on_delete=models.CASCADE, related_name='accessories')
    
    # Details
    description = RichTextField()
    brand = models.CharField(max_length=100, blank=True)
    material = models.CharField(max_length=100, blank=True)
    
    # Sizing
    size_options = models.CharField(max_length=200, blank=True, help_text="e.g., S, M, L, XL")
    color_options = models.CharField(max_length=200, blank=True, help_text="Available colors")
    
    # Pricing & Stock
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    # Status
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Accessories"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Accessory.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum([r.rating for r in ratings]) / len(ratings)
        return 0
    
    def rating_count(self):
        return self.ratings.count()
    
    def in_stock(self):
        return self.stock_quantity > 0


class AccessoryImage(models.Model):
    """Multiple images for accessories"""
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='accessories/')
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    alt_text = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-is_primary', 'order']
    
    def __str__(self):
        return f"Image for {self.accessory.name}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            AccessoryImage.objects.filter(accessory=self.accessory, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class DogRating(models.Model):
    """Ratings for dogs"""
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['dog', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.dog.name} - {self.rating} stars"


class AccessoryRating(models.Model):
    """Ratings for accessories"""
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['accessory', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.accessory.name} - {self.rating} stars"


class Wishlist(models.Model):
    """User wishlists"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    dogs = models.ManyToManyField(Dog, blank=True, related_name='wishlisted_by')
    accessories = models.ManyToManyField(Accessory, blank=True, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Wishlist"


class AdoptionForm(models.Model):
    """Adoption application form"""
    HOUSING_CHOICES = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('farm', 'Farm'),
        ('other', 'Other'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('none', 'No Experience'),
        ('some', 'Some Experience'),
        ('experienced', 'Very Experienced'),
    ]
    
    # Personal Information
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = PhoneNumberField()
    address = models.TextField()
    
    # Dog Selection
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='adoption_applications')
    
    # Adoption Questions
    housing_type = models.CharField(max_length=20, choices=HOUSING_CHOICES)
    own_or_rent = models.CharField(max_length=10, choices=[('own', 'Own'), ('rent', 'Rent')])
    has_yard = models.BooleanField(default=False)
    yard_fenced = models.BooleanField(default=False)
    
    # Experience & Other Pets
    dog_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    current_pets = models.TextField(blank=True, help_text="Describe any current pets")
    
    # Lifestyle
    hours_alone = models.IntegerField(help_text="Hours per day the dog will be alone")
    family_members = models.IntegerField(help_text="Number of people in household")
    children_ages = models.CharField(max_length=100, blank=True, help_text="Ages of children, if any")
    
    # Additional Information
    reason_for_adoption = models.TextField()
    veterinarian_name = models.CharField(max_length=200, blank=True)
    references = models.TextField(blank=True, help_text="Personal references (names and contact)")
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Adoption: {self.full_name} - {self.dog.name}"


class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Customer Information
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Contact Details
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = PhoneNumberField()
    
    # Shipping Address
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='United States')
    
    # Order Details
    order_number = models.CharField(max_length=100, unique=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    
    # Payment
    payment_method = models.CharField(max_length=50, default='Contact Seller')
    payment_confirmed = models.BooleanField(default=False)
    
    # Adoption Form (if applicable)
    adoption_form = models.ForeignKey(AdoptionForm, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Notes
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import random
            import string
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Items in an order"""
    ITEM_TYPE_CHOICES = [
        ('dog', 'Dog/Puppy'),
        ('accessory', 'Accessory'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    
    # For dogs
    dog = models.ForeignKey(Dog, on_delete=models.SET_NULL, null=True, blank=True)
    
    # For accessories
    accessory = models.ForeignKey(Accessory, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        if self.dog:
            return f"{self.dog.name} - ${self.price}"
        return f"{self.accessory.name} x{self.quantity} - ${self.subtotal}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)


class HeroVideo(models.Model):
    """Hero section videos for homepage"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='hero_videos/', help_text="Upload MP4 video")
    thumbnail = models.ImageField(upload_to='hero_videos/thumbnails/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title


class PostAd(models.Model):
    """User-submitted advertisements for pets"""
    AD_STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    AD_TYPE = [
        ('sell', 'Selling'),
        ('adopt', 'Adoption'),
        ('service', 'Pet Service'),
        ('lost', 'Lost Pet'),
        ('found', 'Found Pet'),
    ]
    
    # User Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_ads')
    
    # Ad Details
    ad_type = models.CharField(max_length=20, choices=AD_TYPE)
    title = models.CharField(max_length=200)
    description = RichTextField()
    
    # Pet Details (if applicable)
    pet_type = models.CharField(max_length=100, blank=True, help_text="e.g., Dog, Cat, etc.")
    breed = models.CharField(max_length=100, blank=True)
    age = models.CharField(max_length=50, blank=True)
    
    # Pricing (for selling ads)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Contact
    contact_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField()
    location = models.CharField(max_length=200)
    
    # Status
    status = models.CharField(max_length=20, choices=AD_STATUS, default='pending')
    admin_notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    views = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Posted Ad"
        verbose_name_plural = "Posted Ads"
    
    def __str__(self):
        return f"{self.title} - {self.get_ad_type_display()}"


class PostAdImage(models.Model):
    """Images for posted ads"""
    post_ad = models.ForeignKey(PostAd, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_ads/')
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-is_primary', 'order']
    
    def __str__(self):
        return f"Image for {self.post_ad.title}"


class ContactMessage(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = PhoneNumberField(blank=True, null=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    
    # Response
    is_responded = models.BooleanField(default=False)
    admin_response = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Newsletter(models.Model):
    """Newsletter subscriptions"""
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email

class Testimonial(models.Model):
    """Customer testimonials/reviews for homepage"""
    customer_name = models.CharField(max_length=200)
    customer_image = models.ImageField(upload_to='testimonials/', blank=True, null=True, help_text="Customer photo (optional)")
    location = models.CharField(max_length=200, blank=True, help_text="e.g., New York, USA")
    
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating out of 5 stars"
    )
    review_text = models.TextField(help_text="Customer's review")
    
    # What they purchased (optional)
    purchased_dog = models.ForeignKey(Dog, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    purchased_accessory = models.ForeignKey(Accessory, on_delete=models.SET_NULL, null=True, blank=True, related_name='testimonials')
    
    is_featured = models.BooleanField(default=True, help_text="Show on homepage")
    is_approved = models.BooleanField(default=False, help_text="Approved by admin")
    
    order = models.IntegerField(default=0, help_text="Display order (lower first)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Customer Testimonial"
        verbose_name_plural = "Customer Testimonials"
    
    def __str__(self):
        return f"{self.customer_name} - {self.rating} stars"