from main import ShortenerRepositoryInterface, CollisionException


class InMemoryCollisionRepository(ShortenerRepositoryInterface):
    def __init__(self):
        super().__init__()
        self.storage = {}

    def enforce_collision_next_query(self):
        self.enforce_collision_flag = True

    def get_by_key(self, short_key: str) -> str or bool:
        return self.storage.get(short_key, False)

    def store(self, url_text: str, short_key: str) -> bool:

        if self.storage.get(short_key, None) or self.enforce_collision_flag:
            self.enforce_collision_flag = False
            raise CollisionException("Collision with " + short_key)

        self.storage[short_key] = url_text

        return True
