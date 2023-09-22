from rest_framework.views import APIView
from rest_framework.response import Response
from .middleware import TwoFactorAuthenticationMiddleware


class MyProtectedView(APIView):

    middleware_classes = [TwoFactorAuthenticationMiddleware]

    def get(self, request):
        if request.user.is_authenticated and request.session.get('otp_verified'):
            # User is authenticated, show protected content
            return Response({'message': 'Hello, authenticated user!'})
        else:
            # User is not authenticated, show error message
            return Response({'message': 'Access denied. Please verify your identity using 2FA.'})
        
#The get method checks whether the otp_verified flag is set in the user's session. 
#If the flag is set, the user is considered authenticated and allowed to access the view.
#Otherwise, an error message is returned indicating that the user needs to verify their identity using 2FA before accessing the view.
