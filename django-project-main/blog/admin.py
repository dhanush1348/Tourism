from django.contrib import admin
from .models import BlogCategory, Tag, Post, Comment, PostLike

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'view_count', 'like_count')
    list_filter = ('status', 'categories', 'tags')
    search_fields = ('title', 'content', 'author__email')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at', 'view_count', 'like_count')
    inlines = [CommentInline]
    filter_horizontal = ('categories', 'tags')
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'author', 'content', 'excerpt', 'featured_image')}),
        ('Categories & Tags', {'fields': ('categories', 'tags')}),
        ('SEO', {'fields': ('meta_title', 'meta_description')}),
        ('Status', {'fields': ('status', 'published_at')}),
        ('Statistics', {'fields': ('view_count', 'like_count')}),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__email', 'post__title', 'content')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__email')
    readonly_fields = ('created_at',)
