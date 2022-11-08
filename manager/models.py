from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='balances')
    amount = models.PositiveIntegerField(default=0,
                                         validators=[MinValueValidator(0),
                                                     MaxValueValidator(999_999)])

    def __str__(self):
        return f'{self.user.username} - Balance: {self.amount} c.u.'

    @receiver(post_save, sender=User)
    def create_user_balance(sender, instance, created, **kwargs):
        if created:
            Balance.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_balance(sender, instance, **kwargs):
        instance.balances.save()


class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sum_of_transaction = models.PositiveIntegerField()
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    category = models.TextField(blank=True)
    to_user = models.CharField(max_length=150, blank=True)
    organization = models.CharField(max_length=50, blank=True)
    description = models.TextField(max_length=255, blank=True)


    def __str__(self):
        return f'{self.owner} to {self.category} transfer {self.sum_of_transaction} c.u.'



# class CreditCard(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     number_of_card = models.IntegerField(max_length=16)
#     data = models.CharField(max_length=5)
#     cvv = models.IntegerField(max_length=3)



# class Caties(models.Model):
#     CATEGORIES_CHOICES = (
#         ('Забота о себе', 'Забота о себе'),
#         ('Зарплата', 'Зарплата'),
#         ('Здоровье и фитнес', 'Здоровье и фитнес'),
#         ('Кафе и рестораны', 'Кафе и рестораны'),
#         ('Машина', 'Машина'),
#         ('Образование', 'Образование'),
#         ('Отдых и развлечения', 'Отдых и развлечения'),
#         ('Платежи, комиссии', 'Платежи, комиссии'),
#         ('Покупки: одежда, техника', 'Покупки: одежда, техника'),
#         ('Продукты', 'Продукты'),
#         ('Проезд', 'Проезд'),
#     )
#
#     cat = models.CharField(choices=CATEGORIES_CHOICES, max_length=35)


CATEGORIES_CHOICES = (
    ('Забота о себе', 'Забота о себе'),
    ('Зарплата', 'Зарплата'),
    ('Здоровье и фитнес', 'Здоровье и фитнес'),
    ('Кафе и рестораны', 'Кафе и рестораны'),
    ('Машина', 'Машина'),
    ('Образование', 'Образование'),
    ('Отдых и развлечения', 'Отдых и развлечения'),
    ('Платежи, комиссии', 'Платежи, комиссии'),
    ('Покупки: одежда, техника', 'Покупки: одежда, техника'),
    ('Продукты', 'Продукты'),
    ('Проезд', 'Проезд')
)


# class Catat(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE,
#                                 related_name='catates')
#
#     cat = models.CharField(choices=CATEGORIES_CHOICES, max_length=35)
#     #
#     # def __str__(self):
#     #     return f'{self.user.username} - Balance: {self.amount} c.u.'
#
#     @receiver(post_save, sender=User)
#     def create_user_catat(sender, instance, created, **kwargs):
#         if created:
#             Catat.objects.create(user=instance)
#
#     @receiver(post_save, sender=User)
#     def save_user_catat(sender, instance, **kwargs):
#         instance.catates.save()


