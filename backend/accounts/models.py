from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    poster_url = models.URLField(blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    summary_en = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class UserMovieStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_statuses')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='user_statuses')
    watched = models.BooleanField(default=False)
    watched_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'movie')

    def mark_watched(self):
        self.watched = True
        self.watched_at = timezone.now()
        self.save()
