from tools.utils import convert_image_to_base64
from pathlib import Path

icon_base = Path(__file__).resolve()
"""Setting the icons - all icons have to be base64 i.e. use convert function"""

IP = convert_image_to_base64( icon_base.parent / r'flat/ip.png')
EMAIL = convert_image_to_base64(icon_base.parent / r'flat/email.png')
WEB_PROFILE = convert_image_to_base64(icon_base.parent / r'flat/profile.png')
VKONTAKTE = convert_image_to_base64(icon_base.parent / r'social_media/vkontakte.png')
USERNAME = convert_image_to_base64(icon_base.parent / r'flat/username.png')
TAVILY = convert_image_to_base64(icon_base.parent / r'modules/tavily.png')
WEBPAGE = convert_image_to_base64(icon_base.parent / r'flat/webpage.png')
COMMENT = convert_image_to_base64(icon_base.parent / r'flat/comment.png')
IMAGE = convert_image_to_base64(icon_base.parent / r'flat/image.png')
TARGET = convert_image_to_base64(icon_base.parent / r'flat/target.png')
TAG = convert_image_to_base64(icon_base.parent / r'flat/tag.png')
IDENTIFICATOR = convert_image_to_base64(icon_base.parent / r'flat/identificator.png')