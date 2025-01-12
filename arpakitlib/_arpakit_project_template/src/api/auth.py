from arpakitlib.ar_fastapi_util import api_key_api_auth
from src.core.settings import get_cached_settings

check_with_settings_api_key_api_auth = api_key_api_auth(
    correct_api_key=get_cached_settings().api_correct_api_key
)
