from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.db.models.fields import CharField, EmailField, TextField
from taggit.managers import TaggableManager
from django.urls import reverse
from django.utils.text import slugify
from taggit.models import Tag

# Create your models here.


class Category(models.Model):
    name = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name or not self.name.strip():
            raise ValueError(
                "اسم دسته‌بندی نمی‌تونه خالی باشه یا فقط فاصله داشته باشه."
            )
        self.name = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(
        upload_to="blog_page_home",
        null=True,
        blank=True,
        default="blog_page_home/default.png",
    )
    title = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    content = models.TextField()
    category = models.ManyToManyField("Category")
    tags = TaggableManager(blank=True)
    status = models.BooleanField(default=False)
    counted_views = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean_tags(self):
        current_tags = list(self.tags.names())
        self.tags.clear()
        for name in current_tags:
            clean = slugify(name.strip())
            if clean:
                self.tags.add(clean)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

        self.clean_tags()

    def get_absolute_url(self):
        return reverse("blog_page:single_post", kwargs={"pid": self.id})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=128)
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    massage = models.TextField(default="")
    create_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("blog_page:single_post", kwargs={"pid": self.post.id})

    def clean(self):
        if not self.name.strip():
            raise ValidationError("اسم نباید خالی باشه.")
        if not self.subject.strip():
            raise ValidationError("موضوع نباید خالی باشه.")
