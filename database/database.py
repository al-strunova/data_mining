from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import models


class Database:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        models.Base.metadata.create_all(bind=engine)
        self.maker = sessionmaker(bind=engine)

    def _get_or_create(self, session, model, unique_field, data):
        instance: model = session.query(model).filter_by(
            **{unique_field: data[unique_field]}
        ).first()
        if not instance:
            instance = model(**data)
        return instance

    def _get_or_create_comments(self, session, data: list) -> list:
        result = []
        if data:
            for comment in data:
                comment_author = self._get_or_create(
                    session,
                    models.Author,
                    ["url"],
                    comment["comment"]["user"]["url"],
                    name=comment["comment"]["user"]["full_name"],
                    url=comment["comment"]["user"]["url"],
                )
                db_comment = self._get_or_create(
                    session,
                    models.Comment,
                    models.Comment.id,
                    comment["comment"]["id"],
                    **comment["comment"],
                    **comment["comment"],
                    author=comment_author,
                )
                result.append(db_comment)
                result.extend(
                    self._get_or_create_comments(session, comment["comment"]["children"])
                )

    def create_post(self, data):
        session = self.maker()
        comments = self._get_or_create_comments(session, data["comments_data"])
        post = self._get_or_create(session, models.Post, "url", data["post_data"])
        author = self._get_or_create(session, models.Author, "url", data["author_data"])
        tags = [
            self._get_or_create(session, models.Tag, "url", tag_data)
            for tag_data in data["tags_data"]
        ]
        post.author = author
        post.comments = comments
        post.tags.extend(tags)
        session.add(post)
        try:
            session.commit()
        except Exception as exc:
            print(exc)
            session.rollback()
        finally:
            session.close()

        print(1)
