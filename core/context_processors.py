from .models import SiteSettings, BreedCategory, AccessoryCategory


def site_settings(request):
    """Make site settings available in all templates"""
    try:
        settings = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings = None
    
    return {
        'site_settings': settings,
        'breed_categories': BreedCategory.objects.all()[:10],
        'accessory_categories': AccessoryCategory.objects.all()[:10],
    }


def cart_context(request):
    """Make cart data available in all templates"""
    cart = request.session.get('cart', {})
    cart_count = sum(item['quantity'] for item in cart.values())
    
    cart_total = 0
    for item in cart.values():
        cart_total += float(item['price']) * item['quantity']
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
    }
