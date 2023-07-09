from django.db import models
from users.models import TimeStamp, UserProfile


# Create your models here.


class UserPost(TimeStamp):
    caption = models.CharField(max_length=1000, null=True)
    location = models.CharField(max_length=100, null=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post')
    is_published = models.BooleanField(default=False)


class PostMedia(TimeStamp):

    def get_media_url(instance, filename):
        ext = filename.split('.')[-1]
        return f"post_media/{instance.post.id}_{instance.sequence_index}.{ext}"

    media_file = models.FileField(upload_to=get_media_url)
    sequence_index = models.PositiveSmallIntegerField(default=0)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='media')

    class Meta:
        unique_together = ('post', 'sequence_index')


# TODO: IMPLEMENT REACTIONS ON POSTS

class PostLikes(TimeStamp):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='liked_posts')

    class Meta:
        unique_together = ('post', 'liked_by')


# TODO: IMPLEMENT NESTED COMMENTS
# TODO: IMPLEMENT LIKES ON COMMENTS

class PostComments(TimeStamp):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='commented_posts')
    comment = models.CharField(max_length=1000, null=True)
