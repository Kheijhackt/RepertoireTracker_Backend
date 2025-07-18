from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import secrets

def default_repertoire():
    return {"allPieces": []}

class AppUser(models.Model):
    id = models.AutoField(primary_key=True)  # Now using default auto-increment PK

    username = models.CharField(max_length=150, unique=True)  # Unique & mutable
    display_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # Hashed
    repertoire = models.JSONField(default=default_repertoire, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=64, unique=True, blank=True, null=True)

    def generate_token(self):
        self.token = secrets.token_hex(32)  # 64-character secure token

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.display_name} ({self.username})"