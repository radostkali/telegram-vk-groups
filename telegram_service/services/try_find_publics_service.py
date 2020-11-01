from dataclasses import dataclass
from typing import Optional, List

from vk_service import vk_api
from vk_service.api import VkResponseError

from database.daos.public_dao import PublicDTO


@dataclass
class FoundPublicsDTO:
    not_found_publics: List[str]
    retrieved_public_dto_list: List[PublicDTO]


class TryFindPublicsService:

    def _parse_slug_name(self, slug_or_link: str) -> Optional[str]:
        slug_or_link = slug_or_link.strip(' \n&=/')
        slug_name = slug_or_link

        splited_link = slug_or_link.split('/')
        if len(splited_link) > 1:
            if 'vk.com' not in splited_link or 'm.vk.com' not in splited_link:
                return
            slug_name = splited_link[-1]

        if slug_name.startswith('public'):
            slug_name = slug_name.lstrip('public')

        return slug_name

    def _try_find_public(self, slug_or_link: str) -> Optional[PublicDTO]:
        slug_name = self._parse_slug_name(slug_or_link)
        if not slug_name:
            return

        try:
            public_dto = vk_api.get_public_info_by_slug_name(slug_name)
        except VkResponseError:
            return

        return public_dto

    def execute(self, raw_publics_list: str) -> FoundPublicsDTO:
        publics_to_search = raw_publics_list.split('\n')

        not_found_publics = []
        retrieved_publics = []
        for slug_or_link in publics_to_search:
            public_dto = self._try_find_public(
                slug_or_link=slug_or_link
            )

            if not public_dto:
                not_found_publics.append(slug_or_link)
                continue

            retrieved_publics.append(public_dto)

        found_publics_dto = FoundPublicsDTO(
            not_found_publics=not_found_publics,
            retrieved_public_dto_list=retrieved_publics,
        )
        return found_publics_dto
