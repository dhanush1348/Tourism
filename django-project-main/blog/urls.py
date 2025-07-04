from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('category/<slug:slug>/', views.category_posts, name='category'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag'),
    path('search/', views.post_search, name='search'),
    path('author/<str:username>/', views.author_posts, name='author'),
    path('<slug:slug>/', views.post_detail, name='detail'),
    path('<slug:slug>/like/', views.post_like, name='like'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
] 