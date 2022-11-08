from drf_expences_manager.celery import app
from django.contrib.auth import get_user_model
from manager.models import Transaction
from django.db.models import Max, Min, Avg
from django.db.models.functions import Round
from django.core.mail import send_mail
from drf_expences_manager import settings


@app.task(bind=True)
def send_beat_mail(self):
    users = get_user_model().objects.all()
    mail_subject = "some transactions statistic"
    for user in users:
        trans_count = Transaction.objects.filter(owner=user).count()
        trans_max = Transaction.objects.filter(owner=user).\
                    aggregate(res=Max('sum_of_transaction'))
        trans_min = Transaction.objects.filter(owner=user).\
                    aggregate(res=Min('sum_of_transaction'))['res']
        trans_avg = Transaction.objects.filter(owner=user).\
                    aggregate(res=Round(Avg('sum_of_transaction'), 2))['res']
        send_mail(
            subject=mail_subject,
            message=f'Dear {user.username}, your balance is {user.balances.amount} c.u. '
                    f'You have in total {trans_count} tranactions. '
                    f'Max of transaction was {trans_max["res"]} c.u.'
                    f'Min of transaction was {trans_min} c.u.'
                    f'Avg of transaction was {trans_avg} c.u.'
                    f'Thank you for using our app!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True,
        )
    return f"email was sent to users"
