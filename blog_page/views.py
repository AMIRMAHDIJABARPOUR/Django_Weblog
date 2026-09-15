from .models import Post, Comment
from .forms import CommentModelForm
from django.shortcuts import render, get_object_or_404, redirect

from django.db.models import Q, Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag
from django.contrib import messages


def blog_home(request, category=None, author=None, tag=None):
    posts = posts = Post.objects.annotate(
        comments_count=Count("comment", filter=Q(comment__approved=True))
    ).order_by("-updated_date")
    all_posts = posts
    tag_ids = (
        Post.objects.filter(tags__isnull=False)
        .values_list("tags__id", flat=True)
        .distinct()
    )
    all_tags = Tag.objects.filter(id__in=tag_ids)

    if category:
        posts = posts.filter(category__name__iexact=str(category)).distinct()
    if author:
        posts = posts.filter(
            Q(author__username__icontains=author)
            | Q(author__first_name__icontains=author)
            | Q(author__last_name__icontains=author)
        )
    if tag:
        posts = posts.filter(tags__name__iexact=tag)

    if request.GET.get("s"):
        search_query = request.GET.get("s")
        posts = posts.filter(
            Q(title__icontains=search_query)
            | Q(content__icontains=search_query)
            | Q(author__username__icontains=search_query)
            | Q(category__name__icontains=search_query),
            status=True,
        ).distinct()

    paginator_posts = Paginator(posts, 4)
    page_number = request.GET.get("page")
    page_obj = paginator_posts.get_page(page_number)

    context = {
        "posts": posts,
        "all_posts": all_posts,
        "page_obj": page_obj,
        "page_range": paginator_posts.page_range,
        "tags": all_tags,
    }
    return render(request, "blog/blog-home.html", context)


def single_post(request, pid):
    post = get_object_or_404(Post, pk=pid)

    posts = Post.objects.all().order_by("-updated_date")
    all_tags = Tag.objects.all()

    comments = Comment.objects.filter(post_id=pid, approved=True).order_by(
        "-create_date"
    )

    # Previous post = older post
    previous_post = (
        Post.objects.filter(status=True, created_date__lt=post.created_date)
        .order_by("-created_date")
        .first()
    )

    # Next post = newer post
    next_post = (
        Post.objects.filter(status=True, created_date__gt=post.created_date)
        .order_by("created_date")
        .first()
    )

    if request.method == "POST":
        comment_form = CommentModelForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            messages.success(request, "Your comment has been submitted")

            return redirect("blog_page:single_post", pid=post.id)

    context = {
        "post": post,
        "posts": posts,
        "tags": all_tags,
        "comments": comments,
        "previous_post": previous_post,
        "next_post": next_post,
    }

    return render(request, "blog/blog-single.html", context)
