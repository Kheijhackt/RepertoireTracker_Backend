from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AppUser
from .serializers import AppUserSerializer
from rest_framework.permissions import AllowAny

def get_user_by_token(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return None, Response({'error': 'Token required'}, status=400)

    # Optional: support `Token <token>` format if needed
    token = auth_header.split(" ")[-1].strip()

    try:
        user = AppUser.objects.get(token=token)
        return user, None
    except AppUser.DoesNotExist:
        return None, Response({'error': 'Invalid token'}, status=400)


class SignupView(APIView):
    def post(self, request):
        serializer = AppUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.generate_token()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Invalid username or password'}, status=400)
        
        if user.token is None:
            user.generate_token()
            user.save()

        return Response({
            "username": user.username,
            "display_name": user.display_name,
            "token": user.token
        })

class UserUpdateView(APIView):
    def patch(self, request):
        # Step 1: Get token from header
        token = request.headers.get('Authorization')
        if not token:
            return Response({'error': 'Authorization token required'}, status=401)

        # Step 2: Find user by token
        try:
            user = AppUser.objects.get(token=token)
        except AppUser.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=401)

        # Step 3: Require password in body and verify it
        password = request.data.get('password')
        if not password:
            return Response({'error': 'Password required'}, status=400)
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=400)

        # Step 4: Update display name
        new_display_name = request.data.get('display_name')
        if new_display_name:
            user.display_name = new_display_name

        # Step 5: Update password
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)

        # Step 6: Update username (no 90-day rule)
        new_username = request.data.get('new_username')
        if new_username and new_username != user.username:
            if AppUser.objects.filter(username=new_username).exists():
                return Response({'error': 'Username already taken'}, status=400)
            user.username = new_username

        user.save()
        serializer = AppUserSerializer(user)
        return Response(serializer.data)

    
class BackupView(APIView):
    def post(self, request):
        user, error = get_user_by_token(request)
        if error:
            return error

        repertoire = request.data.get('repertoire')
        if repertoire is None:
            return Response({'error': 'Repertoire required'}, status=400)

        user.repertoire = repertoire
        user.save()
        return Response({'message': 'Backup successful'}, status=200)

class RestoreView(APIView):
    def post(self, request):
        user, error = get_user_by_token(request)
        if error:
            return error

        return Response({'repertoire': user.repertoire}, status=200)

class DeleteAccountView(APIView):
    def delete(self, request):
        user, error = get_user_by_token(request)
        if error:
            return error

        password = request.data.get("password")
        if not password:
            return Response({'error': 'Password required'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Incorrect password'}, status=403)

        user.delete()
        return Response({'message': 'Account deleted successfully.'}, status=200)
