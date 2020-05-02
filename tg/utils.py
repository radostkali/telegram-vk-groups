from typing import Optional, Dict, Union

from vk import vk
from db.crud import (
    check_if_user_exists,
    put_user_in_db,
    check_if_public_exists,
    put_public_in_db,
    link_public_to_user
)


def handle_public_link(link):
    # type: (str) -> Optional[Dict[str, Union[int, str]]]
    splited_link = link.split('/')
    if len(splited_link) > 1:
        if 'vk.com' in splited_link or 'm.vk.com' in splited_link:
            link = splited_link[-1]
        else:
            return None
    link = link.lstrip('public')
    public_info = vk.get_public_info_by_name(link)
    return public_info


def check_or_create_user_in_db(user_id):
    # type: (int) -> None
    user = check_if_user_exists(user_id)
    if not user:
        put_user_in_db(user_id)


def check_or_create_public_in_db(public_info):
    # type: (Dict[str, Union[int, str]]) -> None
    public = check_if_public_exists(public_info['public_id'])
    if not public:
        put_public_in_db(public_info)


def link_public_to_user_in_db(user_id, public_info):
    # type: (int, Dict[str, Union[int, str]]) -> None
    check_or_create_public_in_db(public_info)
    link_public_to_user(user_id, public_info['public_id'])

