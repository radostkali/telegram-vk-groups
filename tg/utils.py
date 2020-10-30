from typing import Optional, Dict, List, Tuple, Any

from vk import VkAPI
from vk.api import PublicDTO, VkResponseError
from db.db_crud_dao import (
    DBCrudDAO,
    get_users_publics_to_refresh,
    update_user_last_refresh,
    get_user_publics,
    remove_user_public_by_id,
)
from tg.msg_media_types import get_post_message


def try_fetch_vk_public(slug_or_link: str) -> Optional[PublicDTO]:
    splited_link = slug_or_link.split('/')
    if len(splited_link) > 1:
        if 'vk.com' not in splited_link:
            return
        slug_or_link = splited_link[-1]

    if slug_or_link.startswith('public'):
        slug_or_link = slug_or_link.lstrip('public')

    try:
        public_dto = VkAPI.get_public_info_by_slug_name(slug_or_link)
    except VkResponseError:
        return

    return public_dto


def check_or_create_user_in_db(
        user_id: int,
        login: str,
        first_name: Optional[str],
        last_name: Optional[str],
) -> None:
    user = DBCrudDAO.check_if_user_exists(user_id)
    if not user:
        DBCrudDAO.create_user(
            user_id=user_id,
            login=login,
            first_name=first_name,
            last_name=last_name,
        )


def check_or_create_public_in_db(public_dto: PublicDTO) -> None:
    public = DBCrudDAO.check_if_public_exists(
        public_id=public_dto.public_id
    )
    if not public:
        DBCrudDAO.create_public(public_dto)


def link_public_to_user_in_db(user_id: int, public_dto: PublicDTO) -> None:
    check_or_create_public_in_db(public_dto=public_dto)
    DBCrudDAO.link_public_to_user(
        user_id=user_id,
        public_id=public_dto.public_id,
    )


def prepare_new_posts() -> List[Tuple[str, Dict[str, Any]]]:
    posts_to_send = []
    users_publics = get_users_publics_to_refresh()
    for user_id, user in users_publics.items():
        last_refresh = user['last_refresh']
        for pub_id in user['publics']:
            users_publics[user_id]['publics'][pub_id]['posts'] = VkAPI.fetch_fresh_posts(pub_id, last_refresh)
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


def list_user_publics(user_id: int) -> str:
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
