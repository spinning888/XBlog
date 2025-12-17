# blog/admin.py
from django.contrib import admin
from .models import Post, Profile, Category, Comment, Favorite, PostLike, CommentLike

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'created_on') # 在列表页显示的字段
    prepopulated_fields = {'slug': ('title',)} # 输入标题时自动填充slug

admin.site.register(Post, PostAdmin)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'author', 'parent', 'created_on')

admin.site.register(Favorite)
admin.site.register(PostLike)
admin.site.register(CommentLike)