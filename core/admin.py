from django.contrib import admin
from django.utils.html import format_html

from .models import (
    SiteSettings, Partner, BreedCategory, AccessoryCategory,
    Dog, DogImage, Accessory, AccessoryImage,
    DogRating, AccessoryRating, Wishlist,
    AdoptionForm, Order, OrderItem, HeroVideo,
    PostAd, PostAdImage, ContactMessage, Newsletter,Testimonial
)


class SingletonModelAdmin(admin.ModelAdmin):
    """Admin for singleton models"""
    def has_add_permission(self, request):
        return not self.model.objects.exists()


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'footer_text')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'whatsapp', 'address', 'business_hours')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'instagram_url', 'twitter_url', 'youtube_url', 'pinterest_url', 'tiktok_url')
        }),
        ('Chat Widget', {
            'fields': ('tawk_property_id', 'tawk_widget_id'),
            'description': 'Configure Tawk.to live chat widget'
        }),
        ('About Us', {
            'fields': ('about_us_content', 'about_us_image')
        }),
        ('Payment Methods Display', {
            'fields': ('show_visa', 'show_mastercard', 'show_paypal', 'show_amex')
        }),
    )


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'website_url', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(BreedCategory)
class BreedCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_featured', 'order', 'dog_count']
    list_editable = ['is_featured', 'order']
    list_filter = ['is_featured']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def dog_count(self, obj):
        return obj.dogs.count()
    dog_count.short_description = 'Dogs'


@admin.register(AccessoryCategory)
class AccessoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'accessory_count']
    list_editable = ['order']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def accessory_count(self, obj):
        return obj.accessories.count()
    accessory_count.short_description = 'Accessories'


class DogImageInline(admin.TabularInline):
    model = DogImage
    extra = 1
    fields = ['image', 'is_primary', 'order', 'alt_text']


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed_category', 'age_months', 'gender', 'price', 'is_sold', 'is_featured', 'created_at']
    list_filter = ['breed_category', 'gender', 'size', 'is_sold', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'color']
    list_editable = ['is_sold', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DogImageInline]
    readonly_fields = ['views', 'average_rating_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'breed_category')
        }),
        ('Details', {
            'fields': ('age_months', 'gender', 'size', 'color', 'description', 'temperament', 'health_status')
        }),
        ('Pricing', {
            'fields': ('price', 'is_negotiable')
        }),
        ('Status', {
            'fields': ('is_sold', 'is_featured', 'is_available_for_adoption')
        }),
        ('Statistics', {
            'fields': ('views', 'average_rating_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def average_rating_display(self, obj):
        avg = obj.average_rating()
        return f"{avg:.1f} / 5.0 ({obj.rating_count()} ratings)"
    average_rating_display.short_description = 'Average Rating'


class AccessoryImageInline(admin.TabularInline):
    model = AccessoryImage
    extra = 1
    fields = ['image', 'is_primary', 'order', 'alt_text']


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_active', 'is_featured', 'created_at']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'brand']
    list_editable = ['is_active', 'is_featured']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AccessoryImageInline]
    readonly_fields = ['views', 'average_rating_display', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category')
        }),
        ('Details', {
            'fields': ('description', 'brand', 'material', 'size_options', 'color_options')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock_quantity')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('views', 'average_rating_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def average_rating_display(self, obj):
        avg = obj.average_rating()
        return f"{avg:.1f} / 5.0 ({obj.rating_count()} ratings)"
    average_rating_display.short_description = 'Average Rating'


@admin.register(DogRating)
class DogRatingAdmin(admin.ModelAdmin):
    list_display = ['dog', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['dog__name', 'user__username', 'review']
    readonly_fields = ['created_at']


@admin.register(AccessoryRating)
class AccessoryRatingAdmin(admin.ModelAdmin):
    list_display = ['accessory', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['accessory__name', 'user__username', 'review']
    readonly_fields = ['created_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'dog_count', 'accessory_count', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['dogs', 'accessories']
    
    def dog_count(self, obj):
        return obj.dogs.count()
    dog_count.short_description = 'Dogs'
    
    def accessory_count(self, obj):
        return obj.accessories.count()
    accessory_count.short_description = 'Accessories'


@admin.register(AdoptionForm)
class AdoptionFormAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'dog', 'email', 'status', 'created_at']
    list_filter = ['status', 'housing_type', 'dog_experience', 'created_at']
    search_fields = ['full_name', 'email', 'dog__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['status']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('user', 'full_name', 'email', 'phone', 'address')
        }),
        ('Dog Selection', {
            'fields': ('dog',)
        }),
        ('Housing Information', {
            'fields': ('housing_type', 'own_or_rent', 'has_yard', 'yard_fenced')
        }),
        ('Experience & Pets', {
            'fields': ('dog_experience', 'current_pets')
        }),
        ('Lifestyle', {
            'fields': ('hours_alone', 'family_members', 'children_ages')
        }),
        ('Additional Information', {
            'fields': ('reason_for_adoption', 'veterinarian_name', 'references')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['item_type', 'dog', 'accessory', 'quantity', 'price', 'subtotal']
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'total_amount', 'status', 'payment_confirmed', 'created_at']
    list_filter = ['status', 'payment_confirmed', 'created_at']
    search_fields = ['order_number', 'full_name', 'email', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    list_editable = ['status', 'payment_confirmed']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip', 'shipping_country')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_confirmed')
        }),
        ('Adoption', {
            'fields': ('adoption_form',),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HeroVideo)
class HeroVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']


class PostAdImageInline(admin.TabularInline):
    model = PostAdImage
    extra = 1
    fields = ['image', 'is_primary', 'order']


@admin.register(PostAd)
class PostAdAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'ad_type', 'status', 'views', 'created_at']
    list_filter = ['ad_type', 'status', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['views', 'created_at', 'updated_at']
    inlines = [PostAdImageInline]
    list_editable = ['status']
    
    fieldsets = (
        ('Ad Information', {
            'fields': ('user', 'ad_type', 'title', 'description')
        }),
        ('Pet Details', {
            'fields': ('pet_type', 'breed', 'age', 'price')
        }),
        ('Contact Information', {
            'fields': ('contact_name', 'contact_email', 'contact_phone', 'location')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes', 'expires_at')
        }),
        ('Statistics', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_responded', 'created_at']
    list_filter = ['is_responded', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_responded']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Response', {
            'fields': ('is_responded', 'admin_response')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    list_editable = ['is_active']


# Add this to the END of /pawsome_pets/core/admin.py

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'location', 'is_featured', 'is_approved', 'order', 'created_at']
    list_editable = ['is_featured', 'is_approved', 'order']
    list_filter = ['is_approved', 'is_featured', 'rating', 'created_at']
    search_fields = ['customer_name', 'location', 'review_text']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_image', 'location')
        }),
        ('Review', {
            'fields': ('rating', 'review_text')
        }),
        ('Purchase Reference (Optional)', {
            'fields': ('purchased_dog', 'purchased_accessory'),
            'classes': ('collapse',)
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_approved', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('purchased_dog', 'purchased_accessory')