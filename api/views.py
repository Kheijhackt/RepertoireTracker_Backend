from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AppUser
from .serializers import AppUserSerializer
from rest_framework.permissions import AllowAny

class SignupView(APIView):
    def post(self, request):
        serializer = AppUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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

        return Response({
            'username': user.username,
            'display_name': user.display_name
        })

class UserUpdateView(APIView):
    def patch(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400)

        try:
            user = AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=400)

        # Update display name
        new_display_name = request.data.get('display_name')
        if new_display_name:
            user.display_name = new_display_name

        # Update password
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)

        # Update username (90-day rule)
        new_username = request.data.get('new_username')
        if new_username and new_username != user.username:
            if not user.can_change_username():
                return Response({'error': 'Username can only be changed every 90 days'}, status=400)
            if AppUser.objects.filter(username=new_username).exists():
                return Response({'error': 'Username already taken'}, status=400)
            user.change_username(new_username)

        user.save()
        serializer = AppUserSerializer(user)
        return Response(serializer.data)
    
class BackupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        repertoire = request.data.get('repertoire')

        if not username or not password or repertoire is None:
            return Response({'error': 'Username, password, and repertoire required'}, status=400)

        try:
            user = AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Invalid username or password'}, status=400)

        user.repertoire = repertoire
        user.save()
        return Response({'message': 'Backup successful'}, status=200)

class RestoreView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password required'}, status=400)

        try:
            user = AppUser.objects.get(username=username)
        except AppUser.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Invalid username or password'}, status=400)

        return Response({'repertoire': user.repertoire}, status=200)


