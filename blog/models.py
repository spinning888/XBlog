# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="分类名称")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="标题")
    slug = models.SlugField(unique=True, verbose_name="URL别名")  # 用于生成好看的URL
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    content = models.TextField(verbose_name="正文")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="分类"
    )
    created_on = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_on = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ['created_on'] # 按时间正序排列（题目要求按时间顺序）

    def __str__(self):
        return self.title

    @property
    def like_count(self) -> int:
        return self.postlike_set.count()

    @property
    def favorite_count(self) -> int:
        return self.favorite_set.count()


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} ❤ {self.post.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} ★ {self.post.title}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="评论内容")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment({self.author.username} on {self.post.title})"

    @property
    def like_count(self) -> int:
        return self.commentlike_set.count()


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "comment")

    def __str__(self):
        return f"{self.user.username} ❤ 评论#{self.comment_id}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.CharField(max_length=200, blank=True, verbose_name='个人宣言')

    def __str__(self):
        return f"Profile({self.user.username})"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # 确保已存在的用户有profile
        Profile.objects.get_or_create(user=instance)