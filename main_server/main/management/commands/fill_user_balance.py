import random

from django.core.management.base import BaseCommand

from main.models import UserModel


class Command(BaseCommand):
    help = 'Fill data in db'

    def handle(self, *args, **options):
        num_users = 10


        for i in range(num_users):
            _user = f'user_{i + 1}'
            _balance = random.randint(0, 5000)
            if not UserModel.objects.filter(username=f'{_user}').exists():
                UserModel.objects.create(username=f'{_user}', balance=_balance)

        print('all users created!')
