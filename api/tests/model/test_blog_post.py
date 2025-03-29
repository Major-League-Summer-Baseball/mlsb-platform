import pytest
from api.errors import ImageDoesNotExist, PlayerDoesNotExist
from api.model import BlogPost
from api.models.shared import convert_date

INVALID_ENTITY = -1

BLOG_DATE = '2020-10-01'
BLOG_TIME = '12:00'
BLOG_TITLE = 'Blog post'
BLOG_SUMMARY = 'This is a summary of an the blog post'
BLOG_HTML = '<p>This is the blog post</p>'


@pytest.mark.usefixtures('image_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_create_blog_post(mlsb_app, player_factory, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        author = player_factory()
        blog = BlogPost(
            author.id,
            BLOG_TITLE,
            BLOG_SUMMARY,
            BLOG_HTML,
            image_id=image.id,
            date=BLOG_DATE,
            time=BLOG_TIME
        )
        assert blog.author_id == author.id
        assert blog.title == BLOG_TITLE
        assert blog.summary == BLOG_SUMMARY
        assert blog.html == BLOG_HTML
        assert blog.image_id == image.id
        assert blog.date == convert_date(BLOG_DATE, BLOG_TIME)


@pytest.mark.usefixtures('image_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_blog_post_requires_author(mlsb_app, image_factory):
    with mlsb_app.app_context():
        with pytest.raises(PlayerDoesNotExist):
            image = image_factory()
            BlogPost(
                INVALID_ENTITY,
                BLOG_TITLE,
                BLOG_SUMMARY,
                BLOG_HTML,
                image_id=image.id,
                date=BLOG_DATE,
                time=BLOG_TIME
            )


@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_blog_post_requires_valid_image(mlsb_app, player_factory):
    with mlsb_app.app_context():
        with pytest.raises(ImageDoesNotExist):
            author = player_factory()
            BlogPost(
                author.id,
                BLOG_TITLE,
                BLOG_SUMMARY,
                BLOG_HTML,
                image_id=INVALID_ENTITY,
                date=BLOG_DATE,
                time=BLOG_TIME
            )


@pytest.mark.usefixtures('image_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_update_blog_post(mlsb_app, player_factory, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        new_image = image_factory()
        author = player_factory()
        new_author = player_factory()
        blog = BlogPost(
            author.id,
            'title',
            'summary',
            '<p>html</p>',
            image_id=image.id
        )
        blog.update(
            author_id=new_author.id,
            title=BLOG_TITLE,
            summary=BLOG_SUMMARY,
            html=BLOG_HTML,
            image_id=new_image.id,
            date=BLOG_DATE,
            time=BLOG_TIME
        )
        assert blog.author_id == new_author.id
        assert blog.title == BLOG_TITLE
        assert blog.summary == BLOG_SUMMARY
        assert blog.html == BLOG_HTML
        assert blog.image_id == new_image.id
        assert blog.date == convert_date(BLOG_DATE, BLOG_TIME)


@pytest.mark.usefixtures('image_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_update_blog_post_requires_valid_author(mlsb_app, player_factory, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        new_image = image_factory()
        author = player_factory()
        blog = BlogPost(
            author.id,
            'title',
            'summary',
            '<p>html</p>',
            image_id=image.id
        )
        with pytest.raises(PlayerDoesNotExist):
            blog.update(
                author_id=INVALID_ENTITY,
                title=BLOG_TITLE,
                summary=BLOG_SUMMARY,
                html=BLOG_HTML,
                image_id=new_image.id,
                date=BLOG_DATE,
                time=BLOG_TIME
            )


@pytest.mark.usefixtures('image_factory')
@pytest.mark.usefixtures('player_factory')
@pytest.mark.usefixtures('mlsb_app')
def test_update_blog_post_requires_valid_image(mlsb_app, player_factory, image_factory):
    with mlsb_app.app_context():
        image = image_factory()
        author = player_factory()
        new_author = player_factory()
        blog = BlogPost(
            author.id,
            'title',
            'summary',
            '<p>html</p>',
            image_id=image.id
        )
        with pytest.raises(ImageDoesNotExist):
            blog.update(
                author_id=new_author.id,
                title=BLOG_TITLE,
                summary=BLOG_SUMMARY,
                html=BLOG_HTML,
                image_id=INVALID_ENTITY,
                date=BLOG_DATE,
                time=BLOG_TIME
            )
