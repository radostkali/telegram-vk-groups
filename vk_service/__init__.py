from vk_service.api import VkApi
from vk_service.loggers import (
    VkApiRequestDebugLogger,
    VkApiRequestLogger,
    VkApiErrorDebugLogger,
    VkApiErrorLogger,
)

import settings

if settings.DEBUG:
    api_info_logger = VkApiRequestDebugLogger()
    api_error_logger = VkApiErrorDebugLogger()
else:
    api_info_logger = VkApiRequestLogger()
    api_error_logger = VkApiErrorLogger()

vk_api = VkApi(
    info_logger=api_info_logger,
    error_logger=api_error_logger,
    vk_api_key=settings.VK_API_KEY,
)
