from django.db import models
from django.db.models import deletion
from django.db.models.aggregates import Sum
from django.urls import reverse
from embed_video.fields import EmbedVideoField

class Post(models.Model):
    text = models.TextField(blank=False, null=False, default='')
    title = models.CharField(max_length=128, blank=False, default='')
    #votes = models.IntegerField(blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('accounts.User', on_delete=deletion.PROTECT, related_name='posts')
    image = models.ImageField(upload_to='posts_images/', null=True, blank=True)
    video = EmbedVideoField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:details", args={self.pk,})

    @property
    def score(self):
        return self.votes.aggregate(Sum('value'))['value__sum'] or 0

class Vote(models.Model):
    class Meta:
        unique_together = ('user', 'post')

    PLUS = 1
    MINUS = -1
    VALUE_CHOICES = (
        (PLUS, '+'),
        (MINUS, '-'),
    )

    value = models.SmallIntegerField(choices=VALUE_CHOICES)
    user = models.ForeignKey('accounts.User', on_delete=deletion.PROTECT, related_name='votes')
    post = models.ForeignKey(Post, on_delete=deletion.CASCADE, related_name='votes')

    def __str__(self):
        return "{user} ocenił na {vote} wrzutę {post}".format(user=self.user, vote=self.value, post=self.post)