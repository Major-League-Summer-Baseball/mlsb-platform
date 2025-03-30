from flask import render_template
from sqlalchemy import desc
from api.authentication import get_user_information
from api.cached_items import get_upcoming_games
from api.model import BlogPost
from api.website import website_blueprint


@website_blueprint.route("/website//news/<int:year>")
def blog_posts(year):
    posts = BlogPost.query.order_by(desc(BlogPost.date)).all()
    return render_template(
        "website/index.html",
        title='League news',
        year=year,
        show_more=False,
        posts=[post.json() for post in posts],
        user_info=get_user_information(),
    )


@website_blueprint.route("/website//news/<int:blog_post_id>/<int:year>")
def blog_post(year, blog_post_id):
    post = BlogPost.query.get(blog_post_id)
    if post is None:
        return render_template(
            "website/notFound.html",
            title="Blog post not found",
            year=year,
            games=get_upcoming_games(year),
            user_info=get_user_information()
        )
    return render_template(
        "website/blog_post.html",
        title=post.title,
        year=year,
        post=post.json(),
        user_info=get_user_information(),
    )
