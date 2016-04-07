from django.test import TestCase, LiveServerTestCase
from .models import Surl, User, Profile


class ModelTest(TestCase):

    def setUp(self):
        self.u = User.objects.create_user('test_user', '1@1.com', '123')
        Profile.objects.create(user=self.u)
        s = Surl()
        s.user = self.u
        s.url = 'http://www.example.com'
        s.save()
        self.s = s

    # def test_primary_key_collision(self):
    #     existing_key = self.s.slug
    #     s = Surl.objects.create(slug=existing_key, url='http://www.example.org', user=self.u)
    #     self.assertNotEqual(existing_key, s.slug)

    def test_anonymous_user_creating_surl(self):
        s = Surl()
        s.url = 'http://www.example.com'
        s.save()
        self.assertEqual(s.user.username, 'surl_system')

    def test_logged_in_user_creating_surl(self):
        pass  # Done in setUp

    def test_surl_count_increment(self):
        initial_count = self.s.count
        self.s.increase_count()
        self.assertEqual(Surl.objects.get(pk=self.s.pk).count, initial_count + 1)

    def test_profile_count_consistency(self):
        initial_count = self.u.profile.count
        self.s.increase_count()
        self.assertEqual(User.objects.get(pk=self.u.pk).profile.count, initial_count + 1)

    def test_profile_count_deleted_surl(self):
        self.s.increase_count()
        initial_count = User.objects.get(pk=self.u.pk).profile.count
        self.s.delete()
        self.assertEqual(User.objects.get(pk=self.u.pk).profile.count, initial_count)


class LiveTest(LiveServerTestCase):
    pass
