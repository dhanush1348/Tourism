from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Post, BlogCategory, Tag, Comment, PostLike

def post_list(request):
    posts = Post.objects.filter(status='published')
    categories = BlogCategory.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        'categories': categories,
        'tags': tags
    })

def category_posts(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = Post.objects.filter(status='published', categories=category)
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts
    })

def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status='published', tags=tag)
    return render(request, 'blog/tag_posts.html', {
        'tag': tag,
        'posts': posts
    })

def post_search(request):
    query = request.GET.get('q', '')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            status='published'
        )
    else:
        posts = Post.objects.none()
    return render(request, 'blog/post_search.html', {
        'query': query,
        'posts': posts
    })

def author_posts(request, username):
    posts = Post.objects.filter(status='published', author__username=username)
    return render(request, 'blog/author_posts.html', {
        'posts': posts,
        'author': username
    })

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = Comment.objects.filter(post=post, is_approved=True, parent=None)
    related_posts = Post.objects.filter(
        status='published',
        categories__in=post.categories.all()
    ).exclude(id=post.id)[:3]
    
    # Increment view count
    post.view_count += 1
    post.save()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'related_posts': related_posts
    })

@login_required
def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    
    if not created:
        like.delete()
        post.like_count -= 1
    else:
        post.like_count += 1
    post.save()
    
    return JsonResponse({
        'likes': post.like_count,
        'liked': created
    })

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        content = request.POST.get('content')
        
        if content:
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                parent_id=parent_id if parent_id else None,
                is_approved=True  # Auto-approve for now
            )
            messages.success(request, 'Your comment has been added.')
            return redirect('blog:detail', slug=slug)
    
    return redirect('blog:detail', slug=slug)
