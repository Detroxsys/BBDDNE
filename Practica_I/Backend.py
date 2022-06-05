#Integrantes 
#Marcela Cruz Larios 
#Yeudiel Lara Moreno
#Pablo David Castillo del Valle
import redis


class DB:
    def __init__(self):
        self.db = redis.Redis(host='127.0.0.1', port=6379, db=0)

    def resetDataBase(self):
        self.db.flushdb()
        return

    # users:username -> {}
    def add_user(self, username, password, is_admin=0):
        user_id = str(self.db.scard("users"))
        A = self.db.sadd("users", username)
        key = "users:" + username
        B = self.db.hmset(key, {
            "password": password,
            "admin": is_admin,
            "id": user_id
        })
        if A and B:
            return user_id
        return None

    def get_user(self, username):
        key = "users:" + username
        response = self.db.hgetall(key)
        return response

    def get_users(self):
        result = self.db.smembers('users')
        return result

    def get_password(self, username):
        key = "users:" + username
        response = self.db.hget(key, "password")
        return response

    def is_admin(self, username):
        key = "users:" + username
        response = self.db.hget(key, "admin")
        return response

    # Añadir, leer y actualizar urls
    # urls:-user:-url-
    def add_url(self, user, url, short_url, cat, status=0):
        key = "urls:" + user + ":" + url
        result = self.db.hmset(key, {
            "short_url": short_url,
            "status": status,
            "category": cat
        })
        return result

    # urls_cat : _user_ : _url_ : _cat_
    def add_url_category(self, user, url, cat):
        key = "urls_cat:" + user + ":" + url
        result = self.db.sadd(key, cat)
        return result

    def get_category(self, user, cat):
        key = "cats:" + user + ":" + cat
        l = self.db.scard(key)
        if l:
            result = self.db.smembers(key)
            return result
        else:
            return -1

    def add_to_category(self, user, cat, url):
        key = "cats:" + user + ":" + cat
        result = self.db.sadd(key, url)
        return result

    def update_category(self, user, cat, url):
        key1 = "urls:" + user + ":" + url
        prevcat = self.db.hget(key1, "category").decode("utf8")
        key2 = "cats:" + user + ":" + prevcat
        key3 = "cats:" + user + ":" + cat
        result = self.db.smove(key2, key3, url.encode("utf8"))
        return

    def update_url_category(self, user, url, cat):
        key = "urls:" + user + ":" + url
        result = self.db.hset(key, "category", cat)
        return result

    def remove_url_category(self, user, url, cat):
        key = "urls_cat:" + user + ":" + url
        result = self.db.srem(key, cat)
        return result

    def get_url_categories(self, user, url):
        key = "urls_cat:" + user + ":" + url
        result = self.db.smembers(key)
        return result

    def get_url_info(self, user, url):
        key = "urls:" + user + ":" + url
        result = self.db.hgetall(key)
        return result

    def update_url_status(self, user, url, status):
        key = "urls:" + user + ":" + url
        result = self.db.hset(key, "status", status)
        return result

    def update_url_categories(self, user, url, cat):
        key = "urls:" + user + ":" + url
        result = self.db.hset(key, "cat", cat)
        return result

    # Añadir y borrar de wishlist
    def add_to_wishlist(self, user, url):
        key = "wishlists:" + user
        result = self.db.sadd(key, url)
        return result

    def get_wishlist(self, user):
        key = "wishlists:" + user
        l = self.db.scard(key)
        if l:
            result = self.db.smembers(key)
            return result
        else:
            return -1

    def get_cat_intersection(self, user1, user2, cat1, cat2):
        key1 = "cats:" + user1 + ":" + cat1
        key2 = "cats:" + user2 + ":" + cat2
        result = self.db.sinter(key1, key2)
        return result

    def remove_from_wishlist(self, user, url):
        key = "wishlists:" + user
        result = self.db.srem(key, url)
        return result

    # Consultar y actualizar listas de categorías
    # cats: _user_ : _cat_
    def get_category(self, user, cat):
        key = "cats:" + user + ":" + cat
        l = self.db.scard(key)
        if l:
            result = self.db.smembers(key)
            return result
        else:
            return -1

    def add_to_category(self, user, cat, url):
        key = "cats:" + user + ":" + cat
        result = self.db.sadd(key, url)
        return result

    def remove_from_category(self, user, cat, url):
        key = "cats:" + user + ":" + cat
        result = self.db.srem(key, url)
        return result