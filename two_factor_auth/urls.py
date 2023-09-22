from django.contrib import admin
from django.urls import path, include
# from captcha_app.middleware import CaptchaMiddleware
# from user.User.UserLogin.views import CustomerLogin, SuperAdminLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('2fa/',include('tfa_otp.urls')),
    path('captcha/',include('captcha_app.urls')),
    path('',include('encryption_app.urls')),

]

# middleware = CaptchaMiddleware(
#     customer_login_view = CustomerLogin.as_view(),
#     superadmin_login_view=SuperAdminLogin.as_view()
# )