from django.db import models
from django.contrib.auth.models import User


class TimeStamp(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Network - edges

#   A ------> B
#   B ------> A
#   A ------> C
#   B ------> C

# user_a -> Who does user_a follow?
# NetworkEdge.objects.filter(from_user=user_a)
# user_a.following.all()  -> [B,C] -> TWO EDGES
# user_a.followers.

# user_b

# TODO: CREATE A SYSTEM FOR PRIVATE PROFILES WHERE USERS CAN DECIDE WHO IS FOLLOWING THEM


class UserProfile(TimeStamp):

    DEFAULT_PROFILE_PIC = "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngw"

    user = models.OneToOneField(User,on_delete=models.CASCADE,null=False,related_name='profile')
    bio = models.CharField(max_length=100,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/',blank=True)
    is_verified = models.BooleanField(default=False)


class NetworkEdge(TimeStamp):
    from_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='following')
    to_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='followers')

    class Meta:
        unique_together = ('from_user','to_user')