from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, \
                   PostDeleteView, UserPostListView, PostLikeToggle, SciencePostListView, \
                   FictionPostListView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/science', SciencePostListView.as_view(), name='science-posts'),
    path('post/fiction', FictionPostListView.as_view(), name='fiction-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.ContactView, name='blog-contact'),
    path('post/<int:pk>/like', PostLikeToggle.as_view(), name='like-toggle'),
    path('post/<int:pk>/comment/', views.PostCommentView, name='post-comment'),
]
