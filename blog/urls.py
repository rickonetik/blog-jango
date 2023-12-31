from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='posts'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/create', views.create_post, name='post-create'),
    path('post/edit/<int:id>/', views.edit_post, name='post-edit'),
    path('post/delete/<int:id>/', views.delete_post, name='post-delete'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('author/<int:author_id>/', views.author_posts, name='author-posts'),
    path('about/', views.about, name='about'),
]
