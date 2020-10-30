from vk.api import VkApi
from vk.loggers import (
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

VkAPI = VkApi(
    info_logger=api_info_logger,
    error_logger=api_error_logger,
)
