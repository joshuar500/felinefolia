from lib.util_sqlalchemy import ResourceMixin, AwareDateTime

from felinefolia.extensions import db

class Comment(ResourceMixin, db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
                                                index=True, nullable=False)

  comment = db.Column(db.String(1028), index=True)

  def __init__(self, **kwargs):
    super(Comment, self).__init__(**kwargs)