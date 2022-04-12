import asyncio
import json
import aiohttp
from core.config import URL_TRANSACTION_MAIN_SERVER
from endpoints.depends import get_transaction_repository
from models.transaction import TransactionUpdate


async def post_transaction(url, session, data):
    transactions = get_transaction_repository()
    try:
        async with session.get(url) as response:
            r = await response.read()
            csrf = json.loads(r).get('csrfmiddlewaretoken')

        header = {'X-CSRFToken': csrf}
        cookies = {'csrftoken': csrf}
        async with session.post(url, data=data, headers=header, cookies=cookies) as response:
            if response.status == 200:
                r = await response.read()
                data = json.loads(r)
                if not data.get('error', ''):
                    id_transaction = int(data.get('id_transaction'))
                    transfer_status = data.get('transfer_status')

                    transfer_update = TransactionUpdate(transfer_status=transfer_status)
                    await transactions.update_transaction(id_transaction, transfer_update)

    except BaseException:
        print("Ваш запрос в очереди")


async def push_transactions():
    while True:
        transactions = get_transaction_repository()
        transactions = await transactions.get_transaction_waiting()
        if transactions:
            async with aiohttp.ClientSession() as session:
                for transaction in transactions:
                    data = {
                        "id_transaction": transaction.id,
                        "id_user": transaction.id_user,
                        "transfer_amount": transaction.transfer_amount,
                        "transfer_choice": transaction.transfer_choice
                    }
                    await post_transaction(URL_TRANSACTION_MAIN_SERVER, session, data)
        await asyncio.sleep(10)
