from database.daos.public_dao import PublicDTO

from vk_service import vk_api


class VkGetPublicService:

    class VkParseContentException(Exception):
        pass

    def get_by_slug_name(self, slug_name: str) -> PublicDTO:
        content = vk_api.get_public_info_by_group_id(
            group_id=slug_name,
        )

        try:
            public_dto = PublicDTO(
                public_id=content['response'][0]['id'],
                public_name=content['response'][0]['name'],
                public_slug_url=slug_name,
            )
        except (ValueError, IndexError) as e:
            raise self.VkParseContentException(e)

        return public_dto
