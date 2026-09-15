from django.contrib import admin
from blog_page.models import Category, Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_date", "updated_date", "status")
    list_filter = ("status", "created_date", "category", "tags")
    fields = (
        "author",
        "image",
        "title",
        "status",
        "content",
        "category",
        "tags",
        "published_date",
    )
    date_hierarchy = "created_date"
    search_fields = ("title",)
    exclude = ("counted_views",)

    def view_on_site(self, obj=None):
        return obj.get_absolute_url()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "subject", "create_date", "approved")
    list_filter = ("create_date", "approved")
    search_fields = ("name", "email", "subject", "massage")

    def view_on_site(self, obj=None):
        return obj.get_absolute_url()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ("name",)

    def view_on_site(self, obj=None):
        return obj.get_absolute_url()
