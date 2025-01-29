from aiogram.filters import Filter

from src.core.settings import get_cached_settings


class NotProdModeFilter(Filter):
    async def __call__(self, *args, **kwargs) -> bool:
        return get_cached_settings().is_mode_type_not_prod
