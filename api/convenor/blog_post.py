from datetime import datetime
from flask import render_template, request, flash, redirect, url_for, session
from sqlalchemy import desc
from api.authentication import get_player_id, require_to_be_convenor
from api.convenor import convenor_blueprint, is_empty
from api.extensions import DB
from api.model import BlogPost
from api.models.shared import split_datetime


@convenor_blueprint.route("blogposts", methods=['DELETE', 'GET'])
@require_to_be_convenor
def blog_posts_page():
    """A page for editing/creating blog_posts"""
    posts = [post.json() for post in BlogPost.query.order_by(desc(BlogPost.date)).all()]
    return render_template(
        "convenor/blogposts.html",
        posts=posts,
    )


@convenor_blueprint.route("blogposts/edit")
@require_to_be_convenor
def edit_blog_post_page():
    """Page to edit a blog post"""
    blog_post_id = request.args.get("blog_post_id", -1)
    blog = BlogPost.query.get(blog_post_id)
    if blog is None:
        session['error'] = f"Blog post does not exist {blog_post_id}"
        return redirect(url_for("convenor.error_page"))
    return render_template(
        'convenor/blogpost.html',
        post=blog.json()
    )


@convenor_blueprint.route("blogposts/new")
@require_to_be_convenor
def new_blog_post_page():
    """Page to create a new blog post"""
    return render_template(
        'convenor/blogpost.html',
        post={
            "blog_post_id": "",
            "title": "",
            "html": "",
            "summary": "",
            "image_id": None,
        }
    )


@convenor_blueprint.route("blogpost/delete/<int:blog_post_id>", methods=["DELETE"])
def delete_blog_post(blog_post_id: int):
    blog_post = BlogPost.query.get(blog_post_id)
    if blog_post is None:
        session['error'] = f"Blog post does not exist {blog_post_id}"
        return redirect(url_for('convenor.error_page'))
    DB.session.delete(blog_post)
    DB.session.commit()
    flash("Blog post was removed")
    return redirect(url_for('convenor.blog_posts_page'))


@convenor_blueprint.route("blogpost/submit", methods=["POST"])
@require_to_be_convenor
def submit_blog_post():
    """Submit edit/create a blog post."""
    author_id = get_player_id()
    summary = request.form.get("summary")
    title = request.form.get("title")
    image_id = request.form.get("image_id")
    html = request.form.get("html")
    blog_post_id = request.form.get("blog_post_id", None)
    (date, time) = split_datetime(datetime.today())
    if image_id is None:
        session['error'] = 'Image is required'
        return redirect(url_for('convenor.error_page'))
    try:
        if is_empty(blog_post_id):
            post = BlogPost(author_id, title, summary, html, image_id, time, date)
            DB.session.add(post)
            flash("Blog post created")
        else:
            post = BlogPost.query.get(blog_post_id)
            if post is None:
                session['error'] = f"Blog post does not exist {blog_post_id}"
                return redirect(url_for('convenor.error_page'))
            post.update(title=title, summary=summary, html=html, image_id=image_id)
            flash("Blog post updated")
    except Exception as e:
        session['error'] = str(e)
        return redirect(url_for('convenor.error_page'))
    DB.session.commit()
    return redirect(url_for("convenor.blog_posts_page"))
