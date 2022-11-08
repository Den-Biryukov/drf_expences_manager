from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


list_of_categories = [
    'Забота о себе', 'Зарплата', 'Здоровье и фитнес', 'Кафе и рестораны',
    'Машина', 'Образование', 'Отдых и развлечения', 'Платежи, комиссии',
    'Покупки: одежда, техника', 'Продукты', 'Проезд'
]


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


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='categories')

    name = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.user} - {self.name}'

    @receiver(post_save, sender=User)
    def create_user_category(sender, instance, created, **kwargs):
        if created:
            for cat in list_of_categories:
                Category.objects.create(user=instance, name=cat)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['user']


class Transaction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    sum_of_transaction = models.PositiveIntegerField()
    time_of_transaction = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    to_user = models.CharField(max_length=150, blank=True)
    organization = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.owner} completed a trans for the amount {self.sum_of_transaction} c.u.'

    class Meta:
        ordering = ['owner']
