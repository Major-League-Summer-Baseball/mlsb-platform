from api.extensions import DB


class Image(DB.Model):
    """
        A class used to store an image stored by some CDN
        Columns:
            id: the unique id
            url: the url to where the image is stored
    """
    id = DB.Column(DB.Integer, primary_key=True)
    url = DB.Column(DB.Text, nullable=False)

    def __init__(self, url: str):
        """Construct a image pointing to some external stored image."""
        self.url = url

    def json(self) -> dict:
        """Returns a jsonserializable object."""
        return {
            'image_id': self.id,
            'url': self.url
        }

    @classmethod
    def does_image_exist(cls, image_id: str) -> bool:
        return Image.query.get(image_id) is not None
