import json
from typing import Dict, Union

import requests
from requests import Response

from vk_service.loggers import VkApiBaseLogger


class VkResponseError(Exception):
    pass


class VkApiBase:
    VK_API_VERSION = '5.103'

    REQUEST_LOG_MSG_TEMPLATE = 'status code: {status_code}, method: {method}, params: {params}'
    API_ERROR_LOG_MSG_TEMPLATE = 'status code: {status_code}, url: {url}, content: {content}'

    def __init__(
            self,
            info_logger: VkApiBaseLogger,
            error_logger: VkApiBaseLogger,
            vk_api_key: str,
    ):
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

        log_message = self.REQUEST_LOG_MSG_TEMPLATE.format(
            status_code=response.status_code,
            method=method,
            params=params,
        )
        self.info_logger.log(log_message)

        if 'error' in content or response.status_code != 200:
            self._handle_api_error(
                response=response,
                url=url,
            )

        return content

    #  def _retry(self, ):  ##  Add retries

    def _handle_api_error(self, response: Response, url: str):
        log_message = self.API_ERROR_LOG_MSG_TEMPLATE.format(
            status_code=response.status_code,
            url=url,
            content=response.content,
        )
        self.error_logger.log(log_message)
        raise VkResponseError(log_message)


class VkApi(VkApiBase):

    def get_wall_posts(
            self,
            public_id: Union[str, int],
            post_count: int,
            offset: int,
    ) -> dict:
        method = 'wall.get'
        params = {
            'owner_id': f'-{public_id}',
            'count': post_count,
            'offset': offset,
            'filter': 'owner',
        }
        content = self._request(method, params)

        return content

    def get_public_info_by_group_id(self, group_id: str) -> dict:
        method = 'groups.getById'
        params = {
            'group_id': group_id
        }
        content = self._request(method, params)

        return content
