from .models import Profile


def ensure_profile_exists(user):
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
