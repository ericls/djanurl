from django.db import models, IntegrityError
from django.db.models import F
from django.contrib.auth.models import User
import shortuuid


def gen_uuid():
    return str(shortuuid.ShortUUID().random(length=5))


class Surl(models.Model):
    slug = models.CharField(max_length=5, default=gen_uuid, primary_key=True, unique=True)
    url = models.URLField()
    user = models.ForeignKey(User, related_name='urls')
    count = models.IntegerField(default=0)
    password = models.CharField(max_length=20, blank=True, default='')

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user = User.objects.get(username='surl_system')
        try:
            super(Surl, self).save(*args, **kwargs)
        except IntegrityError:
            self.slug = gen_uuid()
            self.save()

    def increase_count(self):
        Surl.objects.filter(slug=self.slug).update(count=F('count') + 1)
        Profile.objects.filter(user=self.user).update(count=F('count') + 1)


class Profile(models.Model):
    user = models.OneToOneField(User)
    count = models.IntegerField(default=0)
