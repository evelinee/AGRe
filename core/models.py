from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = PhoneNumberField(null=True)
    is_professor = models.BooleanField(null=True)
    is_student = models.BooleanField(null=True)
    interests = models.ManyToManyField('Interest')


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class Course(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField(null=True)
    timetable = models.CharField(null=True, max_length=300)
    duration = models.CharField(null=True, max_length=30)


class Resource(models.Model):
    BOOK = 'bk'
    ARTICLE = 'art'
    COURSE = 'crs'
    RESOURCE_TYPES = (
        (BOOK, 'Book'),
        (ARTICLE, 'Article'),
        (COURSE, 'Course'),
    )
    uri = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=5, choices=RESOURCE_TYPES)

    def rating(self):
        return self.reviews.all().aggregate(models.Avg('rating'))


class Review(models.Model):
    reviewer = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    item = models.ForeignKey(Resource, related_name='reviews', on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    rating = models.IntegerField()


class Interest(models.Model):
    name = models.CharField(max_length=30)
    selected = False

    def get_clean_name(self):
        return ' '.join(self.name.split('+')).title()
