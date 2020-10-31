from database.daos.user_public_dao import UserPublicDAO


class GetUserPublicsHtmlList:
    def execute(self, user_id: int) -> str:
        public_dto_list = UserPublicDAO.get_user_publics(user_id=user_id)
        public_html_raw_list = []
        for public_number, public_dto in enumerate(public_dto_list, start=1):
            public_html_raw = '{num}. <a href="https://vk.com/{slug}">{name}</a> (<code>{slug}</code>)'.format(
                num=public_number,
                slug=public_dto.public_slug_url,
                name=public_dto.public_name,
            )
            public_html_raw_list.append(public_html_raw)

        publics_html_list = '\n'.join(public_html_raw_list)
        return publics_html_list
