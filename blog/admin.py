from django.contrib import admin
from .models import Post, Comment


# Register your models here.

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created_on', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    # django 5.0 new introduced feature
    # Adding facet counts to the filters
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_on', 'active']
    list_filter = ['active', 'created_on', 'updated_on']
    search_fields = ['name', 'email', 'body']