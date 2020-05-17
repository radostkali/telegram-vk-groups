import json
from typing import Dict, Optional, List, Union
import time

from settings import VK_API_KEY, VK_API_VERSION

import requests


class VkApi:

    def __init__(self, *args, **kwargs):
        self.requiered_params = [
            'access_token={}'.format(VK_API_KEY),
            'v={}'.format(VK_API_VERSION),
        ]

    def get_new_posts(self, pub_id, last_refresh):
        # type: (int, int) -> List[Dict[str, Union[int, str, List[str], bool]]]
        offset = 0
        post_count = 3
        posts = []
        while True:
            new_posts = self.get_wall_last_posts(pub_id, post_count=post_count, offset=offset)
            if not new_posts:
                break
            for post in new_posts:
                if post['timestamp'] > last_refresh or post['is_pinned']:
                    posts.append(post)
                else:
                    return posts
                offset += 3
            time.sleep(0.5)

    def get_wall_last_posts(self, pub_id, post_count=3, offset=0):
        # type: (Union[str, int], int, int) -> Optional[List[Dict[str, Union[int, str, List[str], bool]]]]
        method = 'wall.get'
        params = [
            'owner_id=-{}'.format(pub_id),
            'count={}'.format(post_count),
            'offset={}'.format(offset),
            'filter=owner',
        ]
        response = self._request(method, params)
        if 'error' in response:
            self._api_error_handler(response)
        elif 'response' in response:
            if response['response']['count'] > 0:
                items = response['response']['items']
                posts = []
                for post in items:
                    posts.append({
                        'id': post['id'],
                        'timestamp': post['date'],
                        'text': post['text'],
                        'is_pinned': True if 'is_pinned' in post else False,
                        'pictures': [
                            a['photo']['sizes'][-1]['url'] for a in post['attachments'] if a['type'] == 'photo'
                        ] if 'attachments' in post else []
                    })
                return posts
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
    vk.get_wall_last_posts(124302406)
