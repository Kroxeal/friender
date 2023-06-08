from django.db import models
from django.db.models import F
from datetime import datetime
from django.core.signals import request_finished
from django.db.models.signals import post_save,m2m_changed
from django.dispatch import receiver

STATUS = [
    ('a','available'),
    ('b','busy')
]

SEX = [
    ('m', 'male'),
    ('f', 'female')
]
HOBBIES = [
    ('sp', 'sport'),
    ('tr', 'traveling'),
    ('pt', 'painting'),
    ('cg', 'computer_games'),
    ('sh', 'shopping'),
    ('ph', 'photo'),
    ('ms', 'music')
]
CATEGORY = [
    ('c', 'cafe'),
    ('r', 'restaurant'),
    ('p', 'pub')
]


# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     print("Request finished!")


class Users(models.Model):
    name = models.CharField(max_length=100,verbose_name='имя')
    surname = models.CharField(max_length=100,verbose_name='фамилия')
    age = models.IntegerField(verbose_name='возраст')
    sex = models.CharField(max_length=1, choices=SEX,verbose_name='пол')
    email = models.EmailField(null=True,verbose_name='почта')
    city = models.CharField(max_length=100, default='Minsk',verbose_name='город')

    class Meta:
        indexes = [
            models.Index(fields=["age", "name"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-name"]),
            # models.Index(fields=["age"]),
            models.Index(fields=["-age"]),
            models.Index(fields=["name", '-sex']),
            # models.Index(fields=["age", 'sex']),
        ]
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.name


class Host(Users):
    max_spend_value = models.PositiveIntegerField(null=True)
    status = models.CharField(choices=STATUS, max_length=1, default='a')

    def __str__(self):
        return f"{self.name} ({self.max_spend_value})"
    class Meta:
        verbose_name_plural = 'Приглашающие'



class Guest(Users):
    min_bill_value = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.name} ({self.min_bill_value})"

    class Meta:
        verbose_name_plural = 'Гости'


class Passport(models.Model):
    passport_id = models.CharField(max_length=10, unique=True)
    date_create = models.DateTimeField(auto_now_add=datetime.now())
    user = models.OneToOneField('Users', on_delete=models.CASCADE)

    def __str__(self):
        return self.passport_id


class Hobbies(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=2, choices=HOBBIES)
    user = models.ManyToManyField("Users")

    def __str__(self):
        return str(self.name)


class Arrangements(models.Model):
    host = models.ForeignKey('Host', on_delete=models.CASCADE, null=True)
    guest = models.ForeignKey('Guest', on_delete=models.CASCADE, null=True)
    establishments = models.ForeignKey('Establishments', on_delete=models.CASCADE)


class Establishments(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY)
    address = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.name}"


class Rating(models.Model):
    rating = models.PositiveIntegerField()
    description = models.CharField(max_length=255)

    class Meta:
        abstract = True


class EstablishmentsRating(Rating):
    establishment = models.ForeignKey('Establishments', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.establishment)


class UserRating(Rating):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="photo_ratings", null=True)

    def __str__(self):
        return str(self.rating)


# @receiver(post_save, sender=Users)
def user_created(sender, instance, **kwargs):
    print('signal work')
    print(sender)
    print(instance)
    print(instance.age)
    hobby = Hobbies.objects.get(id=1)
    instance.hobbies_set.add(hobby)

#
post_save.connect(receiver=user_created, sender=Users)