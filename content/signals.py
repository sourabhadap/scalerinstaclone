from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import UserPost, PostMedia, PostLikes, PostComments


@receiver(post_save, sender=PostMedia)
def process_media(sender, instance, **kwargs):
    print("Inside post process media signal")


@receiver(post_save, sender=UserPost)
def send_new_post_notification(sender, instance, **kwargs):
    print("Send new post notification signal")


@receiver(post_save, sender=PostComments)
def profanity_filter(sender, instance, **kwargs):
    print("Profanity filter signal")


@receiver(post_save, sender=PostComments)
def send_new_comment_notification(sender, instance, **kwargs):
    print("Send new comment notification signal")