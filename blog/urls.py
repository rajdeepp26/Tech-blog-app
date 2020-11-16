from django.urls import path
from . import views 
# we will do a direct import for class based views
from .views import (
	PostListView, 
	PostDetailView,
	PostCreateView,
	PostUpdateView,
	PostDeleteView,
    UserPostListView
)


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'), # replaced 'views.home' with 'PostListView.as_view()' 
    # .as_view() is the convention

    # once we click on a post we should get to a detail view of post
    # like for post 1 the url pattern will be like "home/post/1"
    # for post 2 it will be "home/post/2"
    # so our URL PATTERn will contain a variable
    # so django allow us to add VARIABLE to our actual route
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),

    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
]
