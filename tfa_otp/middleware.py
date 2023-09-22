from django.core.mail import send_mail
import random
import string
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from user.User.UserLogin.models import UserLogin

class TwoFactorAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Hello Middleware")
        user = request.user
        session = request.session
        if user.is_authenticated and not session.get('otp_verified'):
            try:
                user_login = user.userlogin
            except UserLogin.DoesNotExist:
                # UserLogin instance does not exist, continue as usual
                return self.get_response(request)

            if user_login.two_factor_auth:
                if request.method == 'POST' and 'otp' in request.POST:
                    # User has submitted the OTP for verification
                    otp = request.POST['otp']
                    if session.get('otp') == otp:
                        # OTP matches, mark as verified in session
                        session['otp_verified'] = True
                        # Redirect to original view
                        return self.get_response(request)
                    else:
                        # OTP does not match, show error message
                        return JsonResponse({'status': 'error', 'response_code': 400, 'message': 'Invalid OTP'})
                else:
                    if request.method == 'POST':
                        # Generate OTP and send it to user via email
                        otp = self.generate_otp()
                        self.send_otp(user, otp)
                        # Store the OTP in session for later verification
                        session['otp'] = otp
                        # Return the OTP as an API response
                        return JsonResponse({'status': 'success', 'response_code': 200, 'message': 'OTP sent to your email.'})
                    else:
                        # Return an error message if the API is called without a POST request
                        return JsonResponse({'status': 'error', 'response_code': 400, 'message': 'Invalid request method'})
            else:
                # Two-factor authentication not enabled, continue as usual
                return self.get_response(request)
        return self.get_response(request)

    def generate_otp(self):
        # Generate a random 6-digit OTP
        return ''.join(random.choices(string.digits, k=6))

    def send_otp(self, user, otp):
        # Send the OTP to the user via email
        subject = 'Your OTP for Two-Factor Authentication'
        message = f'Hi {user.username},\n\nYour OTP is {otp}.\n\nPlease enter this code to verify your identity.\n\nThank you,\nThe Two-Factor Authentication System'
        from_email = 'sidrabazarcommerce@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def render_otp_verification(self, request):
        session = request.session
        if request.method == 'POST':
            # Verify the OTP entered by the user
            otp = request.POST.get('otp')
            if otp == session.get('otp'):
                session['otp_verified'] = True
                return JsonResponse({'status': 'success', 'response_code': 200, 'message': 'OTP verification success.'})
            else:
                return JsonResponse({'status': 'error', 'response_code': 400, 'message': 'Invalid OTP'})
        else:
            # Render the OTP verification form for the user to enter the OTP
            otp = session.get('otp')
            if otp:
                # The OTP has already been generated and sent, show the verification form
                return JsonResponse({'status': 'sucess', 'response_code': 200, 'message': 'Verified'})
            else:
                # The OTP has not been generated and sent yet, show an error message
                return JsonResponse({'status': 'error', 'response_code': 400, 'message': 'OTP has not been sent.'})




