from typing import Optional, Dict, Union, List, Tuple, Any

from vk import vk
from db.crud import (
    check_if_user_exists,
    put_user_in_db,
    check_if_public_exists,
    put_public_in_db,
    link_public_to_user,
    get_users_publics_to_refresh,
    update_user_last_refresh,
    get_user_publics,
    remove_user_public_by_id,
)
from tg.msg_media_types import get_post_message


def handle_public_link(link):
    # type: (str) -> Optional[Dict[str, Union[int, str]]]
    splited_link = link.split('/')
    if len(splited_link) > 1:
        if 'vk.com' in splited_link or 'm.vk.com' in splited_link:
            link = splited_link[-1]
        else:
            return None
    if 'public' in link[:6]:
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


def prepare_new_posts():
    # type: () -> List[Tuple[str, Dict[str, Any]]]
    posts_to_send = []
    users_publics = get_users_publics_to_refresh()
    for user_id, user in users_publics.items():
        last_refresh = user['last_refresh']
        for pub_id in user['publics']:
            users_publics[user_id]['publics'][pub_id]['posts'] = vk.get_new_posts(pub_id, last_refresh)
            for post in users_publics[user_id]['publics'][pub_id]['posts']:
                post_to_send = get_post_message(
                    post=post,
                    user_id=user_id,
                    pub_name=users_publics[user_id]['publics'][pub_id]['name'],
                    pub_id=pub_id,
                )
                posts_to_send.append(post_to_send)
        update_user_last_refresh(user_id)
    return posts_to_send


def list_user_publics(user_id):
    # type: (int) -> str
    publics = get_user_publics(user_id=user_id)
    nums_pubs = ['{}) {}'.format(e + 1, p) for e, p in enumerate(publics.values())]
    return '\n'.join(nums_pubs)


def remove_public_by_number(user_id, pub_num):
    # type (int, int) -> bool
    publics = get_user_publics(user_id=user_id)
    if not 0 < pub_num <= len(publics):
        return None
    public_ids = [p for p in publics.keys()]
    removed = remove_user_public_by_id(user_id, public_ids[pub_num - 1])
    if removed:
        return publics[public_ids[pub_num - 1]]
