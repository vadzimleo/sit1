from django.urls import path
from . import views
from .views import User_posts_view as upv
#, User_posts_pag as upp
#from .views import Posts_view

#routs are: 
urlpatterns = [
    #routs (handled by views) are:
    #path('', views.home, name = 'blog-home'),
    path('', views.Posts_view.as_view(), name = 'blog-home'),
    path('user/<str:name>/', views.User_posts_view, name = 'user-posts'),
    #path('list_posts/<int:page>/', upp, name='user-posts-pag'),
    #Field 'id' expected a number but got 'word', thus not necessarily put <int:pk>
    path('post/<int:pk>/', views.Post_view.as_view(), name = 'post'),
    path('post/<pk>/update/', views.Update_post.as_view(), name = 'update-post'),
    path('post/new/', views.Create_post.as_view(), name='create-post'),
    path('post/<pk>/delete/', views.Delete_post.as_view(), name = 'delete-post'),
    path('about/', views.about, name = 'blog-about'),
]