# blog/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, PostLike, Favorite, Comment
from markdown import markdown
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.text import slugify, Truncator
from django.utils.html import strip_tags
import re
from html import unescape
from .forms import PostForm
from .forms import AvatarForm, ProfileInfoForm
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

# 首页：文章列表
def post_list(request):
    q = request.GET.get('q', '').strip()
    queryset = Post.objects.select_related('author', 'category').all()
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(author__username__icontains=q) | Q(category__name__icontains=q)
        )

    # 最新发布的在最上面
    queryset = queryset.order_by('-created_on')

    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, 5)  # 每页5条
    page_obj = paginator.get_page(page_number)

    # 为列表页构建 Markdown 摘要：移除代码块/行内代码，转纯文本后截取 140 字
    for p in page_obj.object_list:
        try:
            _html = markdown(p.content, extensions=['fenced_code', 'codehilite'])
            # 移除 <pre>...</pre> 代码块
            _html = re.sub(r'<pre\b[^>]*>.*?</pre>', ' ', _html, flags=re.I | re.S)
            # 移除行内 <code>...</code>
            _html = re.sub(r'<code\b[^>]*>.*?</code>', ' ', _html, flags=re.I | re.S)
            _text = strip_tags(_html)
            _text = unescape(_text)
            _text = re.sub(r'\s+', ' ', _text).strip()
            p.excerpt = Truncator(_text).chars(140)
        except Exception:
            p.excerpt = Truncator(p.content).chars(140)

    context = {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'q': q,
    }
    return render(request, 'blog/index.html', context)

# 详情页：文章具体内容
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # 将正文用 Markdown 渲染，支持围栏代码块与高亮
    html_content = markdown(
        post.content,
        extensions=['fenced_code', 'codehilite']
    )
    # 评论表单
    comment_form = CommentForm()
    # 顶级评论（其余通过模板显示回复）
    top_comments = post.comments.filter(parent__isnull=True).select_related('author')

    # 当前用户对文章的互动状态
    user_liked = False
    user_favorited = False
    if request.user.is_authenticated:
        user_liked = PostLike.objects.filter(user=request.user, post=post).exists()
        user_favorited = Favorite.objects.filter(user=request.user, post=post).exists()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'html_content': mark_safe(html_content),
        'comment_form': comment_form,
        'top_comments': top_comments,
        'user_liked': user_liked,
        'user_favorited': user_favorited,
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('blog:post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post: Post = form.save(commit=False)
            post.author = request.user
            # 基于标题生成唯一 slug
            base = slugify(post.title)
            candidate = base
            i = 1
            while Post.objects.filter(slug=candidate).exists():
                i += 1
                candidate = f"{base}-{i}"
            post.slug = candidate
            # 分类：若填写则创建或复用
            cat_name = form.cleaned_data.get('category_name', '').strip()
            if not cat_name:
                cat_name = '未分类'
            category, _ = Category.objects.get_or_create(name=cat_name)
            post.category = category
            post.save()
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form, "mode": "create"})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # 权限：只能作者本人编辑
    if post.author != request.user:
        return redirect("blog:post_detail", slug=post.slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            cat_name = form.cleaned_data.get('category_name', '').strip()
            if cat_name:
                category, _ = Category.objects.get_or_create(name=cat_name)
                post.category = category
            post.save()
            return redirect("blog:post_my_list")
    else:
        initial = {"category_name": post.category.name if post.category else ""}
        form = PostForm(instance=post, initial=initial)
    return render(request, "blog/post_form.html", {"form": form, "mode": "edit", "post": post})

@login_required
def post_my_list(request):
    queryset = Post.objects.filter(author=request.user)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/my_posts.html', {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
    })

@login_required
def profile(request):
    # 当前用户信息与其文章（分页）
    user = request.user
    # 确保存在 Profile，避免 RelatedObjectDoesNotExist
    from .models import Profile
    profile, _created = Profile.objects.get_or_create(user=user)
    queryset = Post.objects.filter(author=user)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(queryset, 10)
    page_obj = paginator.get_page(page_number)
    profile_form = ProfileInfoForm(instance=profile)
    context = {
        'user': user,
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'profile': profile,
        # 优先使用用户上传头像，没有则 None
        'avatar_url': profile.avatar.url if profile and profile.avatar else None,
        'avatar_form': AvatarForm(instance=profile),
        'profile_form': profile_form,
    }
    if request.method == 'POST':
        # 删除头像按钮
        if request.POST.get('action') == 'remove_avatar':
            if profile.avatar:
                # 删除文件并清空字段
                profile.avatar.delete(save=True)
            return redirect('blog:profile')
        # 更新个人宣言
        if request.POST.get('action') == 'update_bio':
            profile_form = ProfileInfoForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('blog:profile')
            context['profile_form'] = profile_form
            return render(request, 'blog/profile.html', context)
        # 上传/更换头像按钮
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # 仅当确实选择了文件时才保存，避免空提交
            if 'avatar' in request.FILES and request.FILES['avatar'].size > 0:
                form.save()
                return redirect('blog:profile')
        context['avatar_form'] = form
    return render(request, 'blog/profile.html', context)


@login_required
def toggle_post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = PostLike.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('blog:post_detail', slug=slug)


@login_required
def toggle_post_favorite(request, slug):
    post = get_object_or_404(Post, slug=slug)
    fav, created = Favorite.objects.get_or_create(user=request.user, post=post)
    if not created:
        fav.delete()
    return redirect('blog:post_detail', slug=slug)


@login_required
def my_favorites(request):
    qs = Post.objects.filter(favorite__user=request.user).select_related('author', 'category').order_by('-created_on')
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'blog/my_favorites.html', {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
    })


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                post=post,
                author=request.user,
                content=form.cleaned_data['content']
            )
    return redirect('blog:post_detail', slug=slug)


@login_required
def reply_comment(request, comment_id):
    parent = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                post=parent.post,
                author=request.user,
                content=form.cleaned_data['content'],
                parent=parent
            )
    return redirect('blog:post_detail', slug=parent.post.slug)


@login_required
def toggle_comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    from .models import CommentLike
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('blog:post_detail', slug=comment.post.slug)