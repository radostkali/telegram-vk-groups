import time
from dataclasses import dataclass
from typing import List, Union

from vk_service import vk_api


@dataclass
class PostDTO:
    id: int
    timestamp: int
    text: str
    is_pinned: bool
    pictures: List[str]


class VkFetchFreshPostsService:
    FETCHING_POSTS_STEP = 5
    FETCHING_POSTS_MAX_STEPS = 3
    SLEEP_BETWEEN_REQUESTS = 0.5

    class VkParseContentException(Exception):
        pass

    def _get_wall_posts(
            self,
            public_id: Union[str, int],
            post_count: int,
            offset: int,
    ) -> List[PostDTO]:
        content = vk_api.get_wall_posts(
            public_id=public_id,
            post_count=post_count,
            offset=offset,
        )

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

        except (ValueError, IndexError) as e:
            raise self.VkParseContentException(e)

        return posts

    def execute(self, public_id: int, from_timestamp: int) -> List[PostDTO]:
        fresh_posts = []
        for step_number in range(self.FETCHING_POSTS_MAX_STEPS):
            offset = self.FETCHING_POSTS_STEP * step_number
            fetched_posts = self._get_wall_posts(
                public_id=public_id,
                post_count=self.FETCHING_POSTS_STEP,
                offset=offset,
            )
            if not fetched_posts:
                return fresh_posts

            for post in fetched_posts:
                if post.timestamp > from_timestamp:
                    if not post.is_pinned:
                        fresh_posts.append(post)
                elif not post.is_pinned:
                    return fresh_posts

            time.sleep(self.SLEEP_BETWEEN_REQUESTS)

        return fresh_posts
