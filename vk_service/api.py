import json
import time
from dataclasses import dataclass
from typing import Dict, List, Union

import requests
from requests import Response

from database.daos.public_dao import PublicDTO
from vk_service.loggers import VkApiBaseLogger


@dataclass
class PostDTO:
    id: int
    timestamp: int
    text: str
    is_pinned: bool
    pictures: List[str]


class VkResponseError(Exception):
    pass


class VkApiBase:
    VK_API_VERSION = '5.103'

    def __init__(
            self,
            info_logger: VkApiBaseLogger,
            error_logger: VkApiBaseLogger,
            vk_api_key: str,
    ) -> None:
        self.requiered_params = {
            'access_token': vk_api_key,
            'v': self.VK_API_VERSION,
        }
        self.info_logger = info_logger
        self.error_logger = error_logger

    @staticmethod
    def _dict_to_params_url_string(params_dict: Dict[str, Union[str, int]]) -> str:
        str_params_list = []
        for key, value in params_dict.items():
            str_params_list.append(
                '{}={}'.format(key, value)
            )
        return '&'.join(str_params_list)

    def _request(self, method: str, params: Dict[str, Union[str, int]]) -> Dict:
        params.update(self.requiered_params)
        raw_params = self._dict_to_params_url_string(params)
        url = 'https://api.vk.com/method/{method}?{params}'.format(
            method=method,
            params=raw_params,
        )

        response = requests.get(url=url)
        content = json.loads(response.content)

        log_message = 'status code: {}, url: {}, content: {}'.format(
            response.status_code, url, content
        )
        self.info_logger.log(log_message)

        if 'error' in content or response.status_code != 200:
            self._api_error_handler(url, response)
            raise VkResponseError

        return content

    #  def _retry(self, ):  ##  Add retries

    def _api_error_handler(self,url: str, response: Response) -> None:
        log_message = 'type: API error, status code: {}, url: {}, content: {}'.format(
            response.status_code, url, response.content
        )
        self.error_logger.log(log_message)

    def _parse_error_handler(self, content: dict) -> None:
        log_message = 'type: PARSE error, content: {}'.format(content)
        self.error_logger.log(log_message)


class VkApi(VkApiBase):

    FETCHING_POSTS_STEP = 5
    FETCHING_POSTS_MAX_STEPS = 3
    SLEEP_BETWEEN_REQUESTS = 0.5

    def _get_wall_posts(
            self,
            public_id: Union[str, int],
            post_count: int,
            offset: int,
    ) -> List[PostDTO]:
        method = 'wall.get'
        params = {
            'owner_id': '-{}'.format(public_id),
            'count': post_count,
            'offset': offset,
            'filter': 'owner',
        }
        content = self._request(method, params)

        posts = []
        try:
            if content['response']['count'] > 0:
                for item in content['response']['items']:
                    pictures = []
                    if 'attachments' in item:
                        for attachment in item['attachments']:
                            if attachment['type'] == 'photo':
                                pictures.append(attachment['photo']['sizes'][-1]['url'])

                    post_dto = PostDTO(
                        id=item['id'],
                        timestamp=item['date'],
                        text=item['text'],
                        is_pinned=bool(item.get('is_pinned')),
                        pictures=pictures,
                    )
                    posts.append(post_dto)

        except (ValueError, IndexError):
            self._parse_error_handler(content)
            raise VkResponseError

        return posts

    def fetch_fresh_posts(self, public_id: int, from_timestamp: int) -> List[PostDTO]:
        fresh_posts = []
        for step_number in range(self.FETCHING_POSTS_MAX_STEPS):
            offset = self.FETCHING_POSTS_STEP * step_number
            fetched_posts = self._get_wall_posts(
                public_id=public_id,
                post_count=self.FETCHING_POSTS_STEP,
                offset=offset,
            )
            if not fetched_posts:
                break

            for post in fetched_posts:
                if post.timestamp > from_timestamp:
                    if not post.is_pinned:
                        fresh_posts.append(post)

                else:
                    break

            time.sleep(self.SLEEP_BETWEEN_REQUESTS)

        return fresh_posts

    def get_public_info_by_slug_name(self, slug_name: str) -> PublicDTO:
        method = 'groups.getById'
        params = {
            'group_id': slug_name
        }
        content = self._request(method, params)

        try:
            public_dto = PublicDTO(
                public_id=content['response'][0]['id'],
                public_name=content['response'][0]['name'],
                public_slug_url=slug_name,
            )
        except (ValueError, IndexError):
            self._parse_error_handler(content)
            raise VkResponseError

        return public_dto
