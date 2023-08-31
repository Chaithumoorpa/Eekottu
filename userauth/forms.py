from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User
from Shop.models import Vendor

class UserRegisterForm(UserCreationForm):
    username= forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username','class':'form-control form-control-lg'}))
    email= forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email','class':'form-control form-control-lg'}))
    password1= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control form-control-lg'}))
    password2= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'form-control form-control-lg'}))
    is_customer = forms.BooleanField(required=False, label="Are you a customer?", widget=forms.RadioSelect(choices=[(True, 'Customer'), (False, 'Vendor')]))

    class Meta:
        model = User
        fields =['username','email']
        
        
class VendorStepOneForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Owner Full Name as per PAN', 'class': 'form-control form-control-lg'}), required=True)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control form-control-lg'}),required=True)
    business_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Business Name as per GST', 'class': 'form-control form-control-lg'}),required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Brief description about the company', 'class': 'form-control form-control-lg'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Business address', 'class': 'form-control form-control-lg'}),required=True)
    contact = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Contact', 'class': 'form-control form-control-lg'}),required=True)
    pan_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'CMMXXXXX7', 'class': 'form-control form-control-lg'}),required=True)
    gst_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'CCCXXXX88XXXXX', 'class': 'form-control form-control-lg'}),required=True)
    
    class Meta:
        model = Vendor
        fields = ['name', 'image', 'business_name', 'description', 'address', 'contact', 'pan_number', 'gst_number']

class VendorStepTwoForm(forms.ModelForm):
    chat_resp_time = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Mention in Days', 'class': 'form-control form-control-lg'}), required=True)
    shipping_on_time = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Mention in Days', 'class': 'form-control form-control-lg'}),required=True)
    authentic_rating= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Mention in Rating', 'class': 'form-control form-control-lg'}))
    days_return = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Mention in Days', 'class': 'form-control form-control-lg'}),required=True)
    warranty_period = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Mention in Months', 'class': 'form-control form-control-lg'}),required=True)
   
    class Meta:
        model = Vendor
        fields = ['chat_resp_time', 'shipping_on_time', 'authentic_rating', 'days_return', 'warranty_period']

class VendorStepThreeForm(forms.ModelForm):
    
    terms_accepted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input','id':'terms_check'}),
        required=True
    )
    
    class Meta:
        model = Vendor
        fields = ['terms_accepted']