from django.db import transaction as transaction_atomic, OperationalError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render

from main.models import UserModel


def main(request):
    users = UserModel.objects.all()
    return render(request, 'main/index.html', context={'objects_list': users})


def transaction_create(data):
    try:
        id_transaction = int(data.get('id_transaction'))
        id_user = int(data.get('id_user'))
        transfer_choice = data.get('transfer_choice')
        transfer_amount = int(data.get('transfer_amount'))

    except BaseException:
        return {"error": "true"}

    object_user = UserModel.objects.filter(pk=id_user).first()

    if not object_user:
        return {"error": "true"}

    if transfer_choice == "withdrawal":
        new_balance = object_user.balance - transfer_amount
        print(new_balance)
        if new_balance < 0:
            status_data = {'id_transaction': id_transaction, 'transfer_status': 'failed'}
            return status_data
        else:
            object_user.balance = new_balance
            status_data = {'id_transaction': id_transaction, 'transfer_status': 'completed'}

    else:
        object_user.balance = object_user.balance + transfer_amount
        status_data = {'id_transaction': id_transaction, 'transfer_status': 'completed'}
    try:
        object_user.save()
    except OperationalError:
        return {"error": "true"}

    return status_data


def transaction(request):
    if request.method == "POST":
        data = request.POST
        with transaction_atomic.atomic():
            status_data = transaction_create(data)
        return JsonResponse(status_data)

    if request.method == "GET":
        csrf_token = get_token(request)
        return JsonResponse({'csrfmiddlewaretoken': csrf_token})
