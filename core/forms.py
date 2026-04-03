from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    AdoptionForm, Order, PostAd, ContactMessage,
    Newsletter, DogRating, AccessoryRating
)


class UserRegistrationForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class AdoptionFormForm(forms.ModelForm):
    """Adoption application form"""
    class Meta:
        model = AdoptionForm
        fields = [
            'full_name', 'email', 'phone', 'address',
            'housing_type', 'own_or_rent', 'has_yard', 'yard_fenced',
            'dog_experience', 'current_pets',
            'hours_alone', 'family_members', 'children_ages',
            'reason_for_adoption', 'veterinarian_name', 'references'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'current_pets': forms.Textarea(attrs={'rows': 3}),
            'reason_for_adoption': forms.Textarea(attrs={'rows': 4}),
            'references': forms.Textarea(attrs={'rows': 3}),
        }


class CheckoutForm(forms.ModelForm):
    """Checkout form"""
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone',
            'shipping_address', 'shipping_city', 'shipping_state',
            'shipping_zip', 'shipping_country',
            'customer_notes'
        ]
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3}),
            'customer_notes': forms.Textarea(attrs={'rows': 3}),
        }


class PostAdForm(forms.ModelForm):
    """Form for posting ads"""
    class Meta:
        model = PostAd
        fields = [
            'ad_type', 'title', 'description',
            'pet_type', 'breed', 'age', 'price',
            'contact_name', 'contact_email', 'contact_phone', 'location'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
        }


class ContactForm(forms.ModelForm):
    """Contact form"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    class Meta:
        model = Newsletter
        fields = ['email']


class DogRatingForm(forms.ModelForm):
    """Dog rating form"""
    class Meta:
        model = DogRating
        fields = ['rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience with this breed...'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }


class AccessoryRatingForm(forms.ModelForm):
    """Accessory rating form"""
    class Meta:
        model = AccessoryRating
        fields = ['rating', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts about this product...'}),
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)])
        }
