from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from .forms import UserRegisterForm
from django.views.generic import View

from django.conf import settings
from django.core.mail import EmailMessage
from .models import User

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.utils.encoding import force_bytes, force_str
from .utils import generate_token
from django.urls import reverse
from django.contrib import messages

from Shop.models import Customer, Vendor
from django.contrib.auth import login, authenticate, logout
# Create your views here.
def register(request):
    
    if request.method == 'POST':
        form=UserRegisterForm(request.POST)
        
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            
            is_customer = form.cleaned_data.get('is_customer')
            
            if is_customer:
                new_user.is_customer=True
            else:
                new_user.is_vendor=True
                
            new_user.save()
                      
            username= form.cleaned_data.get("username")
            
            messages.success(request,f"Hey {username}, Kindly check your mail we sent a verification email.")
            
    
    
            email_subject = "Activate your Account"
            message = render_to_string('userauth/user_activation.html',{
            'user':new_user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token':generate_token.make_token(new_user),
            'is_customer':'customer' if is_customer else 'vendor'
            })
            
            
            email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [new_user.email]
            
            )
            
            email_message.send()
            return redirect('Shop:index')
        else:
            messages.warning(request, form.errors)
    else:
        form=UserRegisterForm()
    
    context={
        'form':form,
    }
    
    return render(request,'userauth/registration.html', context)

from django.db import IntegrityError
class ActivateAccountView(View):
    
    def get(self, request, uidb64, token, is_customer):
        try:
            uid= force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            
        except Exception as e:
            user = None
            
        print(user)
        if user is not None and generate_token.check_token(user,token):
            
            
            if is_customer == 'vendor':
                try:
                    vendor, created = Vendor.objects.get_or_create(user=user)
                    vendor.save()             
                except IntegrityError as e: 
                    print(f"IntegrityError occurred: {e}")
                     
                token=generate_token.make_token(user)
                return redirect('userauth:step_one', uidb64=uidb64, token=token, is_customer=is_customer)
                # If the user is registered as a customer, create the Customer object and save it
                
            elif is_customer == 'customer':
                customer, created = Customer.objects.get_or_create(user=user)
                if created:
                    customer.save()
                
                user.is_active=True
            
                user.save()
            
            login(request, user)
            
            messages.success(request,"Account Activated successfully")
            return redirect('Shop:index')
            
        return render(request, 'userauth/user_auth_fail.html')
    


from .forms import VendorStepOneForm, VendorStepTwoForm, VendorStepThreeForm

from django.core.exceptions import ObjectDoesNotExist

class StepOneView(View):
    def get(self, request, uidb64, token, is_customer):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print('step=one->',user, generate_token.check_token(user, token) )
        if user is not None and is_customer == 'vendor' and generate_token.check_token(user, token):
            form = VendorStepOneForm()
            return render(request, 'vendor/step_one.html', {'form': form})
        else:
            return render(request, 'userauth/user_auth_fail.html')

    def post(self, request, uidb64, token, is_customer):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and is_customer == 'vendor' and generate_token.check_token(user, token):
            form = VendorStepOneForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    vendor = Vendor.objects.get(user=user)
                except ObjectDoesNotExist:
                    vendor = Vendor(user=user)

                
                vendor.name = form.cleaned_data['name']
                vendor.image = form.cleaned_data['image']
                vendor.business_name = form.cleaned_data['business_name']
                vendor.description = form.cleaned_data['description']
                vendor.address = form.cleaned_data['address']
                vendor.contact = form.cleaned_data['contact']
                vendor.pan_number = form.cleaned_data['pan_number']
                vendor.gst_number = form.cleaned_data['gst_number']
                vendor.save()

                token = generate_token.make_token(user)
                return redirect('userauth:step_two', uidb64=uidb64, token=token, is_customer=is_customer)
            else:
                return render(request, 'vendor/step_one.html', {'form': form})
        else:
            return render(request, 'userauth/user_auth_fail.html')


class StepTwoView(View):
    def get(self, request, uidb64, token, is_customer):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print('step=2->',user, generate_token.check_token(user, token) )

        if user is not None and is_customer == 'vendor' and generate_token.check_token(user, token):
            form = VendorStepTwoForm()
            return render(request, 'vendor/step_two.html', {'form': form})
        else:
            return render(request, 'userauth/user_auth_fail.html')
    
    def post(self, request, uidb64, token, is_customer):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and is_customer == 'vendor' and generate_token.check_token(user, token):
            form = VendorStepTwoForm(request.POST)
            if form.is_valid():
                try:
                    vendor = Vendor.objects.get(user=user)
                except ObjectDoesNotExist:
                    return render(request, 'userauth/user_auth_fail.html')

                vendor.chat_resp_time = form.cleaned_data['chat_resp_time']
                vendor.shipping_on_time = form.cleaned_data['shipping_on_time']
                vendor.authentic_rating = form.cleaned_data['authentic_rating']
                vendor.days_return = form.cleaned_data['days_return']
                vendor.warranty_period = form.cleaned_data['warranty_period']
                vendor.save()

                token = generate_token.make_token(user)
                return redirect('userauth:step_three', uidb64=uidb64, token=token, is_customer=is_customer)
            else:
                return render(request, 'vendor/step_two.html', {'form': form})
        else:
            return render(request, 'userauth/user_auth_fail.html')


class StepThreeView(View):
    def get(self, request, uidb64, token, is_customer):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print('step=3->',user, generate_token.check_token(user, token) )

        if user is not None and is_customer == 'vendor' and generate_token.check_token(user, token):
            form = VendorStepThreeForm()
            return render(request, 'vendor/step_three.html', {'form': form})
        else:
            return render(request, 'userauth/user_auth_fail.html')

    def post(self, request, uidb64, token, is_customer):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and is_customer == 'vendor' and generate_token.check_token(user, token):
            form = VendorStepThreeForm(request.POST)
            if form.is_valid():
                try:
                    vendor = Vendor.objects.get(user=user)
                except ObjectDoesNotExist:
                    return render(request, 'userauth/user_auth_fail.html')

                vendor.terms_accepted = form.cleaned_data['terms_accepted']
                vendor.Vendor_status = 'In Review'
                vendor.save()
                
                user.is_active=True
                user.save()
                login(request, user)

                return redirect('Shop:index')  # Replace 'dashboard' with the URL name of your vendor dashboard view
            else:
                return render(request, 'vendor/step_three.html', {'form': form})
        else:
            return render(request, 'userauth/user_auth_fail.html')




def user_login(request):
    
    if request.user.is_authenticated:
        return redirect('Shop:index')
    
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        try:
            user=User.objects.get( email=email)
        except:
            messages.warning(request,f"User with {email} doesnot exists.")
            
        user=authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,"Welcome to Eekottu.")
            return HttpResponseRedirect(reverse('Shop:index'))
        else:
            messages.warning(request,"User doesnot exists")
    
    return render(request,'userauth/user_login.html')

def user_logout(request):
    
    logout(request)
    messages.success(request,"Logged out!")
    
    return HttpResponseRedirect(reverse('userauth:login'))
