from http import HTTPStatus
import logging
import requests
import sys
from requests.exceptions import RequestException

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


def make_request(token, url, payload):
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
        'Authorization': f'{token}'
    }
    request_params = {
        'url': url,
        'headers': headers,
        'json': payload,
        'verify': VERIFY_SSL,
    }

    try:
        logging.debug(f'Начинаем запрос к API: {url}')

        response = requests.post(**request_params)
        logging.info(
            f'Status Code: {response.status_code}, {response.text}'
        )

    except RequestException as error:
        raise ConnectionError(
            f'Ошибка обращения к API: {error}'
        )

    if response.status_code != HTTPStatus.OK:
        raise ApiError(
            f'Ошибка API: {response.status_code}, {response.text}'
        )


def attach_network(network_name, vlan_id, token):
    """Добавляет сети на коммутаторы.

    Параметры:
        network_name(str) - имя сети
        vlan_id(int) - номер vlan
        attach_payload - параметры добавляемой сети
        url(str) - эндпоинт API
    """
    attach_payload = attach_payload_gen(network_name, vlan_id)

    url = f'{BASE_URL}{APPCENTER_URL}/{FABRIC_NAME}/networks/attachments'

    make_request(token, url, attach_payload)


def create_network(username, password):
    """Создает сети.

    Параметры:
        network_name(str) - имя сети
        vlan_id(int) - номер vlan
        payload - параметры создаваемой сети
        url(str) - эндпоинт API
        username(str) - имя пользователя для авторизации в NDFC
        password(str) - пароль пользователя для авторизации в NDFC
    """
    url = f'{BASE_URL}{APPCENTER_URL}/{FABRIC_NAME}/networks'
    for vlan_id in VLANS:
        network_name = f'{NETWORK_NAME}-{str(vlan_id)}'
        network_id = NETWORK_ID + vlan_id

        payload = networks_payload_gen(network_name, network_id, vlan_id)

        token = get_token(username, password)

        try:

            make_request(token, url, payload)
            attach_network(network_name, vlan_id, token)

        except Exception as error:
            message = f'Сбой в работе: {error}'
            logging.error(message)


def main():
    """Основная логика работы скрипта."""
    username = input('Введите логин: ')
    password = input('Введите пароль: ')
    create_network(username, password)


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
