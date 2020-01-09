from django.test import TestCase
from .models import Profile, Post, Comment
from django.contrib.auth.models import User


class PostTestCase(TestCase):
    '''
    class with testcases for all function in imagepost class
    '''

    def setUp(self):
        '''
        creating new objects
        '''
        self.victor = User(username='victor', email='victor@yahoo.com')
        self.victor.save()

        self.car = Post(image='https://ucarecdn.com/505a47e6-769a-40d7-a4ac-b0dea6822723/',
                        name="BMW series", caption='I love BMW cars', posted_by=self.victor, posted_on='12-10-2019')

    def test_save_post(self):
        '''
        testcase that tests on saving a new post
        '''
        self.car.save_image()
        posts = Post.objects.all()
        self.assertEquals(len(posts), 1)

    def test_delete_post(self):
        '''
        testcase that tests on deleting a post
        '''
        self.car.save_image()
        self.car.delete_image()
        posts = Post.objects.all()
        self.assertTrue(len(posts) == 0)

    def test_get_all_posts(self):
        '''
        testcase that tests on getting all posts
        '''
        self.car.save_image()
        final_result = Post.get_all_posts()
        self.assertEquals(len(final_result), 1)

    def test_single_post(self):
        '''
        testcase that test on getting a single post
        '''
        self.car.save_image()
        result = Post.single_image(self.car.id)
        self.assertTrue(result.name == self.car.name)

    def test_get_user_posts(self):
        '''
        testcase that tests on getting a user's posts
        '''
        self.car.save_image()
        self.victor.save()
        user_posts = Post.get_user_posts(self.victor.id)
        self.assertEquals(len(user_posts), 1)

    def test_get_posts_by_name(self):
        '''
        testcase that tests on getting a post by name
        '''
        self.car.save_image()
        found = Post.get_posts('BMW series')
        self.assertEquals(len(found), 1)

    def tearDown(self):
        '''
        Testcase that delete all objects after every test has run
        '''
        Post.objects.all().delete()
        User.objects.all().delete()


class ProfileTestCase(TestCase):
    '''
    class that tests all function in the userprofile
    '''

    def setUp(self):
        '''
        Testcase to create new user profile object for test purposes
        '''
        self.victor = User(username='victor', email='victor@yahoo.com')
        self.victor.save()

        self.car = Post(image='https://ucarecdn.com/505a47e6-769a-40d7-a4ac-b0dea6822723/',
                        name="BMW series", caption='I love BMW cars', posted_by=self.victor, posted_on='12-10-2019')

        self.v_profile = Profile(user=self.victor, bio='Feel goood',
                                 photo="https://ucarecdn.com/505a47e6-769a-40d7-a4ac-b0dea6822723/")
        self.v_profile.save()

    def test_save_profile(self):
        '''
        testcase that tests on saving a new post
        '''
        self.v_profile.save_profile()
        profiles = Profile.objects.all()
        self.assertEquals(len(profiles), 1)

    def test_delete_post(self):
        '''
        testcase that tests on deleting a post
        '''
        self.v_profile.save_profile()
        self.v_profile.delete_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) == 0)

    def tearDown(self):
        '''
        Testcase that delete all objects after every test has run
        '''
        User.objects.all().delete()
        Profile.all().delete()


class CommentsTestCase(TestCase):
    '''
    class that contains testcases for all function under comments class
    '''

    def setUp(self):
        '''
        creates comment object for test purposes
        '''
        self.victor = User(username='victor', email='victor@yahoo.com')
        self.victor.save()

        self.car = Post(image='https://ucarecdn.com/505a47e6-769a-40d7-a4ac-b0dea6822723/',
                        name="BMW series", caption='I love BMW cars', posted_by=self.victor, posted_on='12-10-2019')
        self.car.save()

        self.comment = Comment(
            body="I like it", post=self.car, posted_by=self.victor, posted_on='09-12-2019')
        self.comment.save()

    def test_save_comment(self):
        '''
        tescase to test on saving a new comment
        '''
        self.comment.save_comment()
        comments = Comment.objects.all()
        self.assertEquals(len(comments), 1)

    def tearDown(self):
        '''
        Testcase that delete all objects after every test has run
        '''
        Post.objects.all().delete()
        User.objects.all().delete()
        Comment.objects.all().delete()

    def test_delete_comment(self):
        '''
        testcase to test on deleting a comment
        '''
        self.victor.save()
        self.car.save()
        self.comment.save_comment()
        self.comment.delete_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) == 0)

    def test_update_caption(self):
        '''
        testcase to test on updating a comment
        '''
        self.comment.save_comment()
        updated = Comment.update_caption(self.comment.id, 'its legit')
        self.assertTrue(updated.body == 'its legit')
