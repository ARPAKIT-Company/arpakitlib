from arpakitlib.ar_fastapi_util import base_api_auth

from src.core.settings import get_cached_settings

api_key_with_settings_api_auth = base_api_auth(
    correct_api_keys=get_cached_settings().api_correct_api_key,
    require_correct_api_key=False
)

correct_api_key_with_settings_api_auth = base_api_auth(
    correct_api_keys=get_cached_settings().api_correct_api_key,
    require_correct_api_key=True
)

token_with_settings_api_auth = base_api_auth(
    correct_tokens=get_cached_settings().api_correct_token,
    require_correct_token=False
)

correct_token_with_settings_api_auth = base_api_auth(
    correct_tokens=get_cached_settings().api_correct_token,
    require_correct_token=True
)
