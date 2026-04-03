from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import json

from .models import (
    Dog, DogImage, Accessory, AccessoryImage,
    BreedCategory, AccessoryCategory, SiteSettings,
    Partner, HeroVideo, Wishlist, DogRating, AccessoryRating,
    AdoptionForm, Order, OrderItem, PostAd, PostAdImage,
    ContactMessage, Newsletter,Testimonial
)
from .forms import (
    UserRegistrationForm, AdoptionFormForm, CheckoutForm,
    PostAdForm, ContactForm, NewsletterForm, DogRatingForm,
    AccessoryRatingForm
)


def get_cart(request):
    """Get cart from session"""
    cart = request.session.get('cart', {})
    return cart


def get_cart_total(request):
    """Calculate cart total"""
    cart = get_cart(request)
    total = 0
    for item_id, item_data in cart.items():
        total += float(item_data['price']) * item_data['quantity']
    return total


def get_cart_count(request):
    """Get total items in cart"""
    cart = get_cart(request)
    count = sum(item['quantity'] for item in cart.values())
    return count



def home(request):
    """Homepage with hero video, featured breeds, and adoption flow"""
    context = {
        'hero_videos': HeroVideo.objects.filter(is_active=True)[:3],
        'featured_breeds': BreedCategory.objects.filter(is_featured=True)[:6],
        'featured_dogs': Dog.objects.filter(is_featured=True, is_sold=False)[:8],
        'featured_accessories': Accessory.objects.filter(is_featured=True, is_active=True)[:8],
        'partners': Partner.objects.filter(is_active=True)[:6],
        'recent_dogs': Dog.objects.filter(is_sold=False)[:4],
        'testimonials': Testimonial.objects.filter(is_approved=True, is_featured=True)[:6],  # NEW LINE
    }
    return render(request, 'home.html', context)


def about_us(request):
    """About us page"""
    return render(request, 'about_us.html')


def contact_us(request):
    """Contact us page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact_us')
    else:
        form = ContactForm()
    
    return render(request, 'contact_us.html', {'form': form})


def dog_list(request):
    """List all dogs with filtering and search"""
    dogs = Dog.objects.filter(is_sold=False)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        dogs = dogs.filter(
            Q(name__icontains=search_query) |
            Q(breed_category__name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(color__icontains=search_query)
        )
    
    # Filters
    breed_id = request.GET.get('breed')
    if breed_id:
        dogs = dogs.filter(breed_category_id=breed_id)
    
    gender = request.GET.get('gender')
    if gender:
        dogs = dogs.filter(gender=gender)
    
    size = request.GET.get('size')
    if size:
        dogs = dogs.filter(size=size)
    
    min_price = request.GET.get('min_price')
    if min_price:
        dogs = dogs.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        dogs = dogs.filter(price__lte=max_price)
    
    age_min = request.GET.get('age_min')
    if age_min:
        dogs = dogs.filter(age_months__gte=age_min)
    
    age_max = request.GET.get('age_max')
    if age_max:
        dogs = dogs.filter(age_months__lte=age_max)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        dogs = dogs.order_by('price')
    elif sort_by == 'price_high':
        dogs = dogs.order_by('-price')
    elif sort_by == 'name':
        dogs = dogs.order_by('name')
    else:
        dogs = dogs.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(dogs, 12)
    page_number = request.GET.get('page')
    dogs_page = paginator.get_page(page_number)
    
    context = {
        'dogs': dogs_page,
        'breeds': BreedCategory.objects.all(),
        'search_query': search_query,
    }
    return render(request, 'dogs/dog_list.html', context)


def dog_detail(request, slug):
    """Dog detail page with ratings"""
    dog = get_object_or_404(Dog, slug=slug)
    
    # Increment views
    dog.views += 1
    dog.save(update_fields=['views'])
    
    # Get images
    images = dog.images.all()
    if not images.exists():
        images = None
    
    # Get ratings
    ratings = dog.ratings.all()[:10]
    
    # Check if user has rated
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = DogRating.objects.get(dog=dog, user=request.user)
        except DogRating.DoesNotExist:
            pass
    
    # Rating form
    if request.method == 'POST' and request.user.is_authenticated:
        form = DogRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.dog = dog
            rating.user = request.user
            
            # Update existing rating if exists
            if user_rating:
                user_rating.rating = rating.rating
                user_rating.review = rating.review
                user_rating.save()
                messages.success(request, 'Your rating has been updated!')
            else:
                rating.save()
                messages.success(request, 'Thank you for your rating!')
            
            return redirect('dog_detail', slug=slug)
    else:
        initial_data = {}
        if user_rating:
            initial_data = {'rating': user_rating.rating, 'review': user_rating.review}
        form = DogRatingForm(initial=initial_data)
    
    # Related dogs
    related_dogs = Dog.objects.filter(
        breed_category=dog.breed_category,
        is_sold=False
    ).exclude(id=dog.id)[:4]
    
    context = {
        'dog': dog,
        'images': images,
        'ratings': ratings,
        'rating_form': form,
        'user_rating': user_rating,
        'related_dogs': related_dogs,
    }
    return render(request, 'dogs/dog_detail.html', context)


def accessory_list(request):
    """List all accessories with filtering"""
    accessories = Accessory.objects.filter(is_active=True)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        accessories = accessories.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__icontains=search_query)
        )
    
    # Filters
    category_id = request.GET.get('category')
    if category_id:
        accessories = accessories.filter(category_id=category_id)
    
    min_price = request.GET.get('min_price')
    if min_price:
        accessories = accessories.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        accessories = accessories.filter(price__lte=max_price)
    
    in_stock = request.GET.get('in_stock')
    if in_stock:
        accessories = accessories.filter(stock_quantity__gt=0)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        accessories = accessories.order_by('price')
    elif sort_by == 'price_high':
        accessories = accessories.order_by('-price')
    elif sort_by == 'name':
        accessories = accessories.order_by('name')
    else:
        accessories = accessories.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(accessories, 12)
    page_number = request.GET.get('page')
    accessories_page = paginator.get_page(page_number)
    
    context = {
        'accessories': accessories_page,
        'categories': AccessoryCategory.objects.all(),
        'search_query': search_query,
    }
    return render(request, 'accessories/accessory_list.html', context)


def accessory_detail(request, slug):
    """Accessory detail page with ratings"""
    accessory = get_object_or_404(Accessory, slug=slug)
    
    # Increment views
    accessory.views += 1
    accessory.save(update_fields=['views'])
    
    # Get images
    images = accessory.images.all()
    if not images.exists():
        images = None
    
    # Get ratings
    ratings = accessory.ratings.all()[:10]
    
    # Check if user has rated
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = AccessoryRating.objects.get(accessory=accessory, user=request.user)
        except AccessoryRating.DoesNotExist:
            pass
    
    # Rating form
    if request.method == 'POST' and request.user.is_authenticated:
        form = AccessoryRatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.accessory = accessory
            rating.user = request.user
            
            # Update existing rating if exists
            if user_rating:
                user_rating.rating = rating.rating
                user_rating.review = rating.review
                user_rating.save()
                messages.success(request, 'Your rating has been updated!')
            else:
                rating.save()
                messages.success(request, 'Thank you for your rating!')
            
            return redirect('accessory_detail', slug=slug)
    else:
        initial_data = {}
        if user_rating:
            initial_data = {'rating': user_rating.rating, 'review': user_rating.review}
        form = AccessoryRatingForm(initial=initial_data)
    
    # Related accessories
    related_accessories = Accessory.objects.filter(
        category=accessory.category,
        is_active=True
    ).exclude(id=accessory.id)[:4]
    
    context = {
        'accessory': accessory,
        'images': images,
        'ratings': ratings,
        'rating_form': form,
        'user_rating': user_rating,
        'related_accessories': related_accessories,
    }
    return render(request, 'accessories/accessory_detail.html', context)


def breed_category_detail(request, slug):
    """Dogs by breed category"""
    category = get_object_or_404(BreedCategory, slug=slug)
    dogs = Dog.objects.filter(breed_category=category, is_sold=False)
    
    # Pagination
    paginator = Paginator(dogs, 12)
    page_number = request.GET.get('page')
    dogs_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'dogs': dogs_page,
    }
    return render(request, 'dogs/breed_category.html', context)


def accessory_category_detail(request, slug):
    """Accessories by category"""
    category = get_object_or_404(AccessoryCategory, slug=slug)
    accessories = Accessory.objects.filter(category=category, is_active=True)
    
    # Pagination
    paginator = Paginator(accessories, 12)
    page_number = request.GET.get('page')
    accessories_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'accessories': accessories_page,
    }
    return render(request, 'accessories/accessory_category.html', context)


# Cart Views
def add_to_cart(request, item_type, item_id):
    """Add item to cart"""
    cart = get_cart(request)
    
    if item_type == 'dog':
        dog = get_object_or_404(Dog, id=item_id, is_sold=False)
        cart_key = f"dog_{item_id}"
        
        if cart_key in cart:
            messages.warning(request, 'This dog is already in your cart.')
        else:
            cart[cart_key] = {
                'type': 'dog',
                'id': item_id,
                'name': dog.name,
                'price': str(dog.price),
                'quantity': 1,
                'image': dog.images.first().image.url if dog.images.exists() else None,
            }
            messages.success(request, f'{dog.name} has been added to your cart.')
    
    elif item_type == 'accessory':
        accessory = get_object_or_404(Accessory, id=item_id, is_active=True)
        cart_key = f"accessory_{item_id}"
        
        if cart_key in cart:
            cart[cart_key]['quantity'] += 1
            messages.success(request, f'{accessory.name} quantity updated.')
        else:
            cart[cart_key] = {
                'type': 'accessory',
                'id': item_id,
                'name': accessory.name,
                'price': str(accessory.price),
                'quantity': 1,
                'image': accessory.images.first().image.url if accessory.images.exists() else None,
            }
            messages.success(request, f'{accessory.name} has been added to your cart.')
    
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def cart_view(request):
    """View cart"""
    cart = get_cart(request)
    cart_items = []
    total = 0
    
    for key, item in cart.items():
        subtotal = float(item['price']) * item['quantity']
        cart_items.append({
            'key': key,
            'type': item['type'],
            'id': item['id'],
            'name': item['name'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'subtotal': subtotal,
            'image': item.get('image'),
        })
        total += subtotal
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


def update_cart(request, cart_key):
    """Update cart item quantity"""
    if request.method == 'POST':
        cart = get_cart(request)
        quantity = int(request.POST.get('quantity', 1))
        
        if cart_key in cart:
            if quantity > 0:
                cart[cart_key]['quantity'] = quantity
                messages.success(request, 'Cart updated successfully.')
            else:
                del cart[cart_key]
                messages.success(request, 'Item removed from cart.')
        
        request.session['cart'] = cart
    
    return redirect('cart_view')


def remove_from_cart(request, cart_key):
    """Remove item from cart"""
    cart = get_cart(request)
    
    if cart_key in cart:
        del cart[cart_key]
        messages.success(request, 'Item removed from cart.')
    
    request.session['cart'] = cart
    return redirect('cart_view')


# Wishlist Views
@login_required
def wishlist_view(request):
    """View wishlist"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    context = {
        'wishlist': wishlist,
    }
    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_to_wishlist(request, item_type, item_id):
    """Add item to wishlist"""
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if item_type == 'dog':
        dog = get_object_or_404(Dog, id=item_id)
        if dog in wishlist.dogs.all():
            messages.warning(request, 'This dog is already in your wishlist.')
        else:
            wishlist.dogs.add(dog)
            messages.success(request, f'{dog.name} added to your wishlist.')
    
    elif item_type == 'accessory':
        accessory = get_object_or_404(Accessory, id=item_id)
        if accessory in wishlist.accessories.all():
            messages.warning(request, 'This accessory is already in your wishlist.')
        else:
            wishlist.accessories.add(accessory)
            messages.success(request, f'{accessory.name} added to your wishlist.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def remove_from_wishlist(request, item_type, item_id):
    """Remove item from wishlist"""
    wishlist = get_object_or_404(Wishlist, user=request.user)
    
    if item_type == 'dog':
        dog = get_object_or_404(Dog, id=item_id)
        wishlist.dogs.remove(dog)
        messages.success(request, f'{dog.name} removed from wishlist.')
    
    elif item_type == 'accessory':
        accessory = get_object_or_404(Accessory, id=item_id)
        wishlist.accessories.remove(accessory)
        messages.success(request, f'{accessory.name} removed from wishlist.')
    
    return redirect('wishlist_view')


# Authentication Views
def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created successfully.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


# Adoption & Checkout
def adoption_form_view(request, dog_id):
    """Adoption form for a specific dog"""
    dog = get_object_or_404(Dog, id=dog_id, is_sold=False)
    
    if request.method == 'POST':
        form = AdoptionFormForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.dog = dog
            if request.user.is_authenticated:
                adoption.user = request.user
            adoption.save()
            
            # Store adoption form ID in session for checkout
            request.session['adoption_form_id'] = adoption.id
            
            messages.success(request, 'Adoption form submitted! Please proceed to checkout.')
            return redirect('checkout')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
            }
        form = AdoptionFormForm(initial=initial_data)
    
    context = {
        'form': form,
        'dog': dog,
    }
    return render(request, 'adoption/adoption_form.html', context)


def checkout_view(request):
    """Checkout process with email notifications"""
    cart = get_cart(request)
    
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_view')
    
    # Calculate total
    total = get_cart_total(request)
    
    # Check if any dog in cart requires adoption form
    requires_adoption = any(item['type'] == 'dog' for item in cart.values())
    adoption_form_id = request.session.get('adoption_form_id')
    
    if requires_adoption and not adoption_form_id:
        messages.warning(request, 'Please complete the adoption form before checkout.')
        # Redirect to adoption form for first dog in cart
        for item in cart.values():
            if item['type'] == 'dog':
                return redirect('adoption_form', dog_id=item['id'])
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = total
            
            # Link adoption form if exists
            if adoption_form_id:
                try:
                    adoption_form = AdoptionForm.objects.get(id=adoption_form_id)
                    order.adoption_form = adoption_form
                except AdoptionForm.DoesNotExist:
                    pass
            
            order.save()
            
            # Create order items
            for item in cart.values():
                if item['type'] == 'dog':
                    dog = Dog.objects.get(id=item['id'])
                    OrderItem.objects.create(
                        order=order,
                        item_type='dog',
                        dog=dog,
                        quantity=1,
                        price=dog.price
                    )
                elif item['type'] == 'accessory':
                    accessory = Accessory.objects.get(id=item['id'])
                    OrderItem.objects.create(
                        order=order,
                        item_type='accessory',
                        accessory=accessory,
                        quantity=item['quantity'],
                        price=accessory.price
                    )
            
            # ========== SEND EMAILS ==========
            try:
                # Get site settings for email
                site_settings = SiteSettings.objects.first()
                
                # Send customer confirmation email
                customer_html = render_to_string('emails/order_confirmation_customer.html', {
                    'order': order,
                    'site_settings': site_settings,
                })
                
                customer_email = EmailMultiAlternatives(
                    subject=f'Order Confirmation #{order.order_number} - {site_settings.site_name}',
                    body='Thank you for your order!',  # Plain text fallback
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[order.email],
                )
                customer_email.attach_alternative(customer_html, "text/html")
                customer_email.send(fail_silently=True)
                
                # Send admin notification email
                admin_html = render_to_string('emails/order_notification_admin.html', {
                    'order': order,
                    'site_settings': site_settings,
                })
                
                admin_email = EmailMultiAlternatives(
                    subject=f'🔔 New Order #{order.order_number} - Action Required',
                    body=f'New order received from {order.full_name}',  # Plain text fallback
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.ADMIN_EMAIL],
                )
                admin_email.attach_alternative(admin_html, "text/html")
                admin_email.send(fail_silently=True)
                
            except Exception as e:
                # Log error but don't stop the order process
                print(f"Email sending error: {e}")
            # ========== END EMAIL SENDING ==========
            
            # Clear cart and adoption form session
            request.session['cart'] = {}
            if 'adoption_form_id' in request.session:
                del request.session['adoption_form_id']
            
            messages.success(request, f'Order #{order.order_number} created successfully! Check your email for confirmation.')
            return redirect('order_confirmation', order_number=order.order_number)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart_items': [
            {
                'name': item['name'],
                'price': float(item['price']),
                'quantity': item['quantity'],
                'subtotal': float(item['price']) * item['quantity'],
            }
            for item in cart.values()
        ],
        'total': total,
    }
    return render(request, 'checkout/checkout.html', context)

def order_confirmation(request, order_number):
    """Order confirmation page with payment popup"""
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
    }
    return render(request, 'checkout/order_confirmation.html', context)


@login_required
def order_history(request):
    """User's order history"""
    orders = Order.objects.filter(user=request.user)
    
    context = {
        'orders': orders,
    }
    return render(request, 'account/order_history.html', context)


@login_required
def order_detail(request, order_number):
    """Order detail page"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'account/order_detail.html', context)


# Post Ad Views
@login_required
def post_ad_create(request):
    """Create a new ad"""
    if request.method == 'POST':
        form = PostAdForm(request.POST)
        if form.is_valid():
            post_ad = form.save(commit=False)
            post_ad.user = request.user
            post_ad.save()
            
            # Handle multiple images
            images = request.FILES.getlist('images')
            for idx, image in enumerate(images):
                PostAdImage.objects.create(
                    post_ad=post_ad,
                    image=image,
                    is_primary=(idx == 0),
                    order=idx
                )
            
            messages.success(request, 'Your ad has been submitted for review.')
            return redirect('post_ad_list')
    else:
        form = PostAdForm()
    
    return render(request, 'post_ad/create.html', {'form': form})


def post_ad_list(request):
    """List all approved ads"""
    ads = PostAd.objects.filter(status='approved')
    
    # Filter by ad type
    ad_type = request.GET.get('type')
    if ad_type:
        ads = ads.filter(ad_type=ad_type)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        ads = ads.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(breed__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(ads, 12)
    page_number = request.GET.get('page')
    ads_page = paginator.get_page(page_number)
    
    context = {
        'ads': ads_page,
        'search_query': search_query,
    }
    return render(request, 'post_ad/list.html', context)


def post_ad_detail(request, pk):
    """Ad detail page"""
    ad = get_object_or_404(PostAd, pk=pk, status='approved')
    
    # Increment views
    ad.views += 1
    ad.save(update_fields=['views'])
    
    context = {
        'ad': ad,
    }
    return render(request, 'post_ad/detail.html', context)


@login_required
def my_ads(request):
    """User's posted ads"""
    ads = PostAd.objects.filter(user=request.user)
    
    context = {
        'ads': ads,
    }
    return render(request, 'post_ad/my_ads.html', context)


# Newsletter
def newsletter_subscribe(request):
    """Newsletter subscription"""
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            Newsletter.objects.get_or_create(email=email)
            messages.success(request, 'Thank you for subscribing to our newsletter!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


# Share functionality
def share_item(request):
    """Generate share data for social media"""
    # This would typically generate share URLs
    # For now, just return to previous page
    return redirect(request.META.get('HTTP_REFERER', 'home'))
