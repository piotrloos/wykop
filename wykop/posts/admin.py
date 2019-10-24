from django.contrib import admin
from wykop.posts.models import Post, Vote

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value')
    search_fields = ('user__username', 'post__title')
    list_filter = ('user', 'post', 'value')

admin.site.register(Post)
admin.site.register(Vote, VoteAdmin)