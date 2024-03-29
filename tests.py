from datetime import datetime, timedelta
import unittest

import app
from app import db, create_app
from app.models import User, Post


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE = 'sqlite://'

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        # self.app.config['SQLALCHEMY_DATABASE_URi'] = 'sqlite://'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.create_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='ll')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='jj', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar'
                                        '/d4c74594d841139328695756648b6bd6'
                                        '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='jj', email='john@example.com')
        u2 = User(username='ss', email='susan@example.com')
        # with app.app_context():
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        # 重新关联实例到当前会话
        # with app.app_context():
        # u1 = db.session.merge(u1)
        # u2 = db.session.merge(u2)

        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # with app.app_context():
            # 创建四个用户
        u1 = User(username='jj', email='john@example.com')
        u2 = User(username='ss', email='susan@example.com')
        u3 = User(username='mm', email='mary@example.com')
        u4 = User(username='dd', email='david@example.com')

        db.session.add_all([u1, u2, u3, u4])
        # db.session.commit()

            # 创建四个帖子
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4, timestamp=now + timedelta(seconds=2))

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

            # 设置关注关系
        u1.follow(u2)  # john关注susan
        u1.follow(u4)  # john关注david
        u2.follow(u3)  # susan关注mary
        u3.follow(u4)  # mary关注david

        db.session.commit()

            # 检查每个用户的关注帖子
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()

        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)
