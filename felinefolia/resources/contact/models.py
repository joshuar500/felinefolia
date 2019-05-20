from sqlalchemy import func
from lib.util_sqlalchemy import ResourceMixin

from felinefolia.extensions import db


class Comment(ResourceMixin, db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
                        index=True, nullable=False)

    comment = db.Column(db.String(1028), index=True)

    def __init__(self, **kwargs):
        super(Comment, self).__init__(**kwargs)

    @classmethod
    def group_and_count_comments(cls):
        """
        Group Comments by User ID

        :return: tuble
        """
        return Comment._group_and_count(Comment, Comment.comment)

    @classmethod
    def _group_and_count(cls, model, field):
        """
        Group results for a specific model and field.

        :param model: Name of the model
        :type model: SQLAlchemy model
        :param field: Name of the field to group on
        :type field: SQLAlchemy field
        :return: dict
        """
        count = func.count(field)
        query = db.session.query(count, field).group_by(field).all()

        results = {
            'query': query,
            'total': model.query.count()
        }

        return results
