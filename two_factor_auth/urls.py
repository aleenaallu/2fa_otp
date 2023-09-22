from django.contrib import admin
from django.urls import path, include
# from captcha_app.middleware import CaptchaMiddleware
# from user.User.UserLogin.views import CustomerLogin, SuperAdminLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('2fa/',include('tfa_otp.urls')),


]

