import argparse
import asyncio
import logging
import sys

import aiohttp

from auth import get_token
from exceptions import ApiError
from parts import attach_payload_gen, networks_payload_gen
from parts import (
    APPCENTER_URL,
    BASE_URL,
    FABRIC_NAME,
    NETWORK_NAME,
    NETWORK_ID,
    VERIFY_SSL,
    VLANS,
)

# =========================
# ACTION CONFIG
# =========================

ACTIONS = {
    'create': {
        'url': f'{BASE_URL}{APPCENTER_URL}/{FABRIC_NAME}/networks',
        'payload_gen': networks_payload_gen
    },
    'attach': {
        'url': f'{BASE_URL}{APPCENTER_URL}/{FABRIC_NAME}/networks/attachments',
        'payload_gen': attach_payload_gen
    }
}

# =========================
# ASYNC REQUEST
# =========================

async def make_request(session, token, url, payload):
    """Обращается к API NDFC.

    Параметры:
        payload - параметры создаваемого/изменяемого объекта
        headers(dict) - параметры заголовка запроса
        request_params(dict) - параметры для выполнения запроса к API
        token(str) - токен для обращения к API
        url(str) - эндпоинт API

    Если ответ от API получить не удалось, выбрасывается исключение
    """

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    try:
        async with session.post(
            url,
            json=payload,
            headers=headers,
            ssl=VERIFY_SSL
            ) as resp:
            text = await resp.text()
            logging.info(f'Status Code: {resp.status}, Response: {text}')
            if resp.status != 200:
                raise ApiError(f'Ошибка API: {resp.status}, {text}')
    except Exception as e:
        logging.error(f'Ошибка запроса к {url}: {e}')
        raise

# =========================
# EXECUTE ACTION
# =========================

async def execute_action(
        session, action, network_name, vlan_id,token
    ):
    """Определяет payload и url 
    для выполнения запроса к API в зависимости от действия.

    Инициирует запрос к API, вызывая функцию make_request
    и передает ей подготовленные данные.

    Параметры:
        action(str) - требуемое действие
        network_name(str) - имя сети
        vlan_id(int) - номер vlan
        token(str) - токен для обращения к API
    """
    action_cfg = ACTIONS[action]

    payload_gen = action_cfg['payload_gen']
    url = action_cfg['url']

    # задает payload взависимости от действия
    if action == 'create':
        network_id = NETWORK_ID + vlan_id
        payload = payload_gen(network_name, network_id, vlan_id)
    if action == 'attach':
        payload = payload_gen(network_name, vlan_id)

    await make_request(session, token, url, payload)

# =========================
# PROCESS NETWORKS
# =========================

async def process_networks(username, password, actions):
    """Выполняет операции с сетями и получает токен авторизации.

    Параметры:
        action(str) - требуемое действие
        network_name(str) - имя сети
        vlan_id(int) - номер vlan
        token(str) - токен для обращения к API
    """

    token = get_token(username, password)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for vlan_id in VLANS:
            network_name = f'{NETWORK_NAME}-{vlan_id}'
            logging.info(f'Обработка VLAN {vlan_id}')

            for action in actions:
                tasks.append(
                    execute_action(
                        session,
                        action,
                        network_name,
                        vlan_id,
                        token
                    )
                )

        # запуск задач
        await asyncio.gather(*tasks, return_exceptions=False)

# =========================
# CLI
# =========================

def main():
    parser = argparse.ArgumentParser(description='NDFC network automation')
    parser.add_argument(
        '--actions',
        nargs='+',
        choices=ACTIONS.keys(),
        default=list(ACTIONS.keys()),
        help='Список действий'
    )
    args = parser.parse_args()

    username = input('Введите логин: ')
    password = input('Введите пароль: ')

    asyncio.run(process_networks(username, password, args.actions))

# =========================
# ENTRYPOINT
# =========================

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('app.log', mode='a', encoding='utf-8')
        ]
    )
    main()
