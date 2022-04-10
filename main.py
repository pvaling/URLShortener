import os
from base64 import urlsafe_b64encode

from sqlalchemy.exc import IntegrityError

from sql_app.crud import create_url, get_url_by_short_url
from sql_app.schemas import ShortUrlCreate


class URL:
    def __init__(self, urlstr: str):
        # url validate
        self.validate()
        self.url = urlstr

    def validate(self) -> bool:
        return True  #todo

    def __repr__(self):
        return self.url


class ShortenerRepositoryInterface:
    def __init__(self):
        pass

    def get_by_key(self, short_key: str) -> str or bool:
        raise NotImplementedError()

    def store(self, url_text: str, short_key: str) -> bool:
        raise NotImplementedError()


class CollisionException(Exception):
    pass

class RepositoryTooManyCollisionFailure(Exception):
    pass


class URLShortener:
    def __init__(self, repo: ShortenerRepositoryInterface):
        self.repo = repo

    @staticmethod
    def get_short_string(input_string) -> str:
        return urlsafe_b64encode(os.urandom(6)).decode('utf-8')

    def zip(self, url: URL) -> str:
        short_key = None

        collision_retry = 5
        while collision_retry:
            try:
                short_key = self.get_short_string(input_string=url.url)
                self.repo.store(url_text=url.url, short_key=short_key)
                break
            except CollisionException:
                collision_retry -= 1

        if collision_retry == 0:
            raise RepositoryTooManyCollisionFailure

        return short_key

    def unzip(self, short_key: str) -> str:
        return self.repo.get_by_key(short_key=short_key)


class InMemoryRepository(ShortenerRepositoryInterface):
    def __init__(self):
        super().__init__()
        self.storage = {}

    def get_by_key(self, short_key: str) -> str or bool:
        return self.storage.get(short_key, False)

    def store(self, url_text: str, short_key: str) -> bool:

        if self.storage.get(short_key, None):
            raise CollisionException("Collision with " + short_key)

        self.storage[short_key] = url_text

        return True


class SQLRepository(ShortenerRepositoryInterface):
    def __init__(self, db):
        super().__init__()
        self.db = db

    def get_by_key(self, short_key: str) -> str or bool:
        res = get_url_by_short_url(db=self.db, short_url=short_key)
        return res.url

    def store(self, url_text: str, short_key: str) -> bool:
        url = ShortUrlCreate(url=url_text)
        try:
            create_url(db=self.db, url=url, short=short_key)
        except IntegrityError as e:
            if e.orig.args[0] == 'UNIQUE constraint failed: urls.short':
                self.db.rollback()
                raise CollisionException("Collision with " + short_key)

        return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url_shortener = URLShortener(repo=InMemoryRepository())
