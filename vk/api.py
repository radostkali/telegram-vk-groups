import json
from typing import Dict, Optional, List, Union

from settings import VK_API_KEY, VK_API_VERSION

import requests


class VkApi:

    def __init__(self, *args, **kwargs):
        self.requiered_params = [
            'access_token={}'.format(VK_API_KEY),
            'v={}'.format(VK_API_VERSION),
        ]

    def get_wall_last_post(self, group_id):
        # type: (Optional[str, int]) -> Optional[Dict, None]
        method = 'wall.get'
        params = [
            'owner_id=-{}'.format(group_id),
            'count=1',
            'filter=owner',
        ]
        response = self._request(method, params)
        if 'error' in response:
            self._api_error_handler(response)
        elif 'response' in response:
            if response['response']['count'] > 0:
                post = response['response']['items'][0]
                last_post = {
                    'id': post['id'],
                    'timestamp': post['date'],
                    'text': post['text'],
                    'is_pinned': post['is_pinned'],
                    'pictures': (
                        a['photo']['sizes'][-1]['url'] for a in post['attachments'] if a['type'] == 'photo'
                    )
                }
                return last_post
        return

    def get_public_info_by_name(self, public_name):
        # type: (str) -> Optional[Dict[str, Union[int, str]]]
        method = 'groups.getById'
        params = [
            'group_id={}'.format(public_name)
        ]
        response = self._request(method, params)
        if 'error' in response:
            self._api_error_handler(response)
            return None
        elif 'response' in response:
            public_info = {
                'public_id': response['response'][0]['id'],
                'public_name': response['response'][0]['name'],
            }
            return public_info

    def _request(self, method, params):
        # type: (str, List) -> Dict
        params = params + self.requiered_params
        raw_params = '&'.join(params)
        url = 'https://api.vk.com/method/{method}?{params}'.format(method=method, params=raw_params)
        response = requests.get(url=url)
        return json.loads(response.content)

    def _api_error_handler(self, response):
        pass


if __name__ == '__main__':
    vk = VkApi()
    vk.get_wall_last_post(124302406)
