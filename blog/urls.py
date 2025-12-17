from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),          # 首页
    path('new/', views.post_create, name='post_create'),  # 先于 slug 路由
    path('my/', views.post_my_list, name='post_my_list'), # 我的文章列表
    path('me/', views.profile, name='profile'),           # 个人信息页
    path('favorites/', views.my_favorites, name='my_favorites'),  # 我的收藏
    # 互动操作
    path('<slug:slug>/like/', views.toggle_post_like, name='post_like'),
    path('<slug:slug>/favorite/', views.toggle_post_favorite, name='post_favorite'),
    path('<slug:slug>/comment/', views.add_comment, name='comment_add'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='comment_reply'),
    path('comment/<int:comment_id>/like/', views.toggle_comment_like, name='comment_like'),
    path('<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('<slug:slug>/', views.post_detail, name='post_detail') # 详情页，最后匹配
]
