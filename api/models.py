from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

class AppUser(models.Model):
    username = models.CharField(max_length=150, primary_key=True)
    display_name = models.CharField(max_length=150)
    password = models.CharField(max_length=128)  # Hashed
    repertoire = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True, blank=True)  # Username change only

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def can_change_username(self):
        if not self.modified_at:
            return True
        return timezone.now() - self.modified_at >= timezone.timedelta(days=90)

    def change_username(self, new_username):
        if self.can_change_username():
            self.modified_at = timezone.now()
            self.username = new_username
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.display_name} ({self.username})"
