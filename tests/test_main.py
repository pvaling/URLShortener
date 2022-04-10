from unittest import TestCase

from main import InMemoryRepository, URLShortener, URL, SQLRepository

# Algorithm
# 1. Validate URL
# 2.
from sql_app import models
from sql_app.database import SessionLocal, engine
from tests.mocks import InMemoryCollisionRepository

RAISE_COLLISION = True
RAISE_COLLISION_INDEX = 2

'''
Algorithm

Store scenario:
1. Validate URL
2. Get URL hash of length 5
2.1 Check for collisions
4. Return Hash to client
3. Async write hash and url into DB and place it into fast cache

Retrieve scenario:
1. Get hash from user
2. Lookup fast cache for URL. If not found look into slow DB
3. Return URL to user


'''

class TestURLShortner(TestCase):
    def test_zip_unzip_memory(self):

        url_shortener = URLShortener(repo=InMemoryRepository())

        sample_pairs = [
            ['https://revolut.com/page1.html', None],
            ['https://sberbank.ru/page1.html', None]
        ]

        for sample_pair in sample_pairs:
            url_obj = URL(urlstr=sample_pair[0])
            short_code = url_shortener.zip(url=url_obj)
            sample_pair[1] = short_code

        for sample_pair in sample_pairs:
            url_obj = url_shortener.unzip(short_key=sample_pair[1])
            self.assertEqual(url_obj, sample_pair[0])

    def test_zip_unzip_sql(self):
        models.Base.metadata.create_all(bind=engine)
        url_shortener = URLShortener(repo=SQLRepository(db=SessionLocal()))

        sample_pairs = [
            ['https://revolut.com/page1.html', None],
            ['https://sberbank.ru/page1.html', None]
        ]

        for sample_pair in sample_pairs:
            url_obj = URL(urlstr=sample_pair[0])
            short_code = url_shortener.zip(url=url_obj)
            sample_pair[1] = short_code

        for sample_pair in sample_pairs:
            url_obj = url_shortener.unzip(short_key=sample_pair[1])
            self.assertEqual(url_obj, sample_pair[0])



    def test_zip_collision(self):

        collision_repo = InMemoryCollisionRepository()

        url_shortener = URLShortener(repo=collision_repo)

        sample_pairs = [
            ['https://revolut.com/page1.html', None, RAISE_COLLISION],
            ['https://sberbank.ru/page1.html', None, False]
        ]

        for sample_pair in sample_pairs:
            # Collision emulator
            if sample_pair[RAISE_COLLISION_INDEX]:
                collision_repo.enforce_collision_next_query()

            url_obj = URL(urlstr=sample_pair[0])
            short_code = url_shortener.zip(url=url_obj)


            sample_pair[1] = short_code

        for sample_pair in sample_pairs:
            url_obj = url_shortener.unzip(short_key=sample_pair[1])
            self.assertEqual(url_obj, sample_pair[0])


class TestInMemoryRepository(TestCase):
    def test_get_by_key(self):
        repo = InMemoryRepository()

        # Case 1. Check for right return value
        # write some data
        sample_pairs = [
            ('https://revolut.com/page1.html', 'XYZ'),
            ('https://sberbank.ru/page1.html', 'YZC')
        ]
        for sample_pair in sample_pairs:
            self.assertEqual(True, repo.store(url_text=sample_pair[0], short_key=sample_pair[1]),
                             msg='Wrong return type after in memory repo insert')

        # Case 2. Check for value exists in repository
        self.assertEqual(repo.get_by_key(sample_pairs[0][1]), sample_pairs[0][0],
                         msg='InMemory repo doesnt return expected url')


    def test_store(self):
        # self.fail()
        pass
