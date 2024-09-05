from django.contrib import admin
from .models import Category, Goods, PriceHistory, Comment, ImageModel


class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 0
    can_delete = False
    readonly_fields = ['price', 'date']


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = [
        'author', 'author_name', 'author_profile_picture',
        'body', 'rating', 'created', 'updated'
    ]


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'rating', 'times_bought']
    search_fields = ['title', 'category__title']
    inlines = [PriceHistoryInline, CommentInline]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['goods', 'price', 'date']
    list_filter = ['goods']
    search_fields = ['goods__title']
    ordering = ['goods']
    readonly_fields = ['goods', 'price', 'date']
    can_delete = False


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'goods', 'rating', 'created']
    search_fields = ['author_name', 'goods__title']
    list_filter = ['goods']
    readonly_fields = [
        'author', 'author_name',
        'author_profile_picture', 'body',
        'rating', 'created', 'updated'
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title",)}


@admin.register(ImageModel)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['comment', 'image']
    search_fields = ['comment__author_name', 'comment__goods__title']
