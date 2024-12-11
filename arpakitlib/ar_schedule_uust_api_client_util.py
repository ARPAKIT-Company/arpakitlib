# arpakit

import asyncio
import hashlib
import logging
from datetime import datetime
from typing import Any

import pytz

from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_http_request_util import async_make_http_request
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class ScheduleUUSTAPIClient:
    def __init__(
            self,
            *,
            api_login: str,
            api_password: str | None = None,
            api_password_first_part: str | None = None,
            api_url: str = "https://isu.uust.ru/api/schedule_v2",
            api_proxy_url: str | None = None
    ):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.api_login = api_login
        self.api_password = api_password
        self.api_password_first_part = api_password_first_part
        self.api_url = api_url
        self.api_proxy_url = api_proxy_url
        self.headers = {
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;"
                "q=0.8,application/signed-exchange;v=b3;q=0.7"
            ),
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
            )
        }

    def auth_params(self) -> dict[str, Any]:
        if self.api_password:
            return {
                "login": self.api_login,
                "pass": self.api_password
            }
        elif self.api_password_first_part:
            return {
                "login": self.api_login,
                "pass": self.generate_v2_token(password_first_part=self.api_password_first_part)
            }
        else:
            return {}

    @classmethod
    def hash_token(cls, token: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(token.encode('utf-8'))
        return sha256.hexdigest()

    @classmethod
    def generate_v2_token(cls, password_first_part: str) -> str:
        return cls.hash_token(
            password_first_part + datetime.now(tz=pytz.timezone("Asia/Yekaterinburg")).strftime("%Y-%m-%d")
        )

    async def _async_make_http_get_request(
            self,
            *,
            url: str,
            params: dict | None = None
    ) -> dict[str, Any]:
        response = await async_make_http_request(
            url=url,
            method="GET",
            params=combine_dicts(params, self.auth_params()),
            proxy_url_=self.api_proxy_url,
        )
        json_data = await response.json()
        raise_for_type(json_data, dict)
        return json_data

    async def get_current_week(self) -> int:
        """
        response.json example
        {
            'data': [15]
        }
        """

        json_data = await self._async_make_http_get_request(
            url=self.api_url,
            params={"ask": "get_current_week"}
        )
        return json_data["data"][0]

    async def get_current_semester(self) -> str:
        """
        response.json example
        {
            'data': ['Осенний семестр 2023/2024']
        }
        """

        json_data = await self._async_make_http_get_request(
            url=self.api_url,
            params={"ask": "get_current_semestr"}
        )
        return json_data["data"][0]

    async def get_groups(self) -> list[dict[str, Any]]:
        """
        response.json example
        {
            "data": {
                "4438": {
                    "group_id": 4438,
                    "group_title": "АРКТ-101А",
                    "faculty": "",
                    "course": 1
                }
            }
        }
        """

        json_data = await self._async_make_http_get_request(
            url=self.api_url,
            params={"ask": "get_group_list"}
        )
        return list(json_data["data"].values())

    async def get_group_lessons(self, group_id: int, semester: str | None = None) -> list[dict[str, Any]]:
        params = {
            "ask": "get_group_schedule",
            "id": group_id
        }
        if semester is not None:
            params["semester"] = semester
        json_data = await self._async_make_http_get_request(
            url=self.api_url,
            params=params
        )
        return json_data["data"]

    async def get_teachers(self) -> list[dict[str, Any]]:
        json_data = await self._async_make_http_get_request(
            url=self.api_url,
            params={"ask": "get_teacher_list"}
        )
        return list(json_data["data"].values())

    async def get_teacher_lessons(self, teacher_id: int, semester: str | None = None) -> list[dict[str, Any]]:
        params = {"ask": "get_teacher_schedule", "id": teacher_id}
        if semester is not None:
            params["semester"] = semester
        json_data = await self._async_make_http_get_request(
            url=self.api_url,
            params=params
        )
        return json_data["data"]

    async def check_conn(self):
        await self.get_current_week()

    async def is_conn_good(self):
        try:
            await self.check_conn()
        except Exception as e:
            self._logger.error(e)
            return False
        return True

    async def check_all(self):
        await self.get_groups()
        await self.get_teachers()
        await self.get_current_semester()
        await self.get_current_week()


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())