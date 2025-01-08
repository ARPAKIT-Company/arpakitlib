# arpakit

import asyncio
import hashlib
import logging
from datetime import datetime
from typing import Any

import pytz
from aiohttp import ClientResponse

from arpakitlib.ar_dict_util import combine_dicts
from arpakitlib.ar_http_request_util import async_make_http_request

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
                "pass": self.generate_v2_token()
            }
        else:
            return {}

    @classmethod
    def hash_new_token(cls, token: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(token.encode('utf-8'))
        return sha256.hexdigest()

    @classmethod
    def generate_new_v2_token(cls, password_first_part: str) -> str:
        return cls.hash_new_token(
            password_first_part + datetime.now(tz=pytz.timezone("Asia/Yekaterinburg")).strftime("%Y-%m-%d")
        )

    def generate_v2_token(self) -> str:
        return self.generate_new_v2_token(password_first_part=self.api_password_first_part)

    async def _async_make_http_request(
            self,
            *,
            method: str = "GET",
            url: str,
            params: dict[str, Any] | None = None
    ) -> ClientResponse:
        response = await async_make_http_request(
            method=method,
            url=url,
            headers=self.headers,
            params=combine_dicts(params, self.auth_params()),
            proxy_url_=self.api_proxy_url,
            raise_for_status_=True
        )
        return response

    async def get_current_week(self) -> int:
        """
        response.json example
        {
            'data': [15]
        }
        """

        response = await self._async_make_http_request(
            url=self.api_url,
            params={"ask": "get_current_week"}
        )
        json_data = await response.json()
        return json_data["data"][0]

    async def get_current_semester(self) -> str:
        """
        response.json example
        {
            'data': ['Осенний семестр 2023/2024']
        }
        """

        response = await self._async_make_http_request(
            url=self.api_url,
            params={"ask": "get_current_semestr"}
        )
        json_data = await response.json()
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

        response = await self._async_make_http_request(
            url=self.api_url,
            params={"ask": "get_group_list"}
        )
        json_data = await response.json()
        return list(json_data["data"].values())

    async def get_group_lessons(self, group_id: int, semester: str | None = None) -> list[dict[str, Any]]:
        params = {
            "ask": "get_group_schedule",
            "id": group_id
        }
        if semester is not None:
            params["semester"] = semester
        response = await self._async_make_http_request(
            url=self.api_url,
            params=params
        )
        json_data = await response.json()
        return json_data["data"]

    async def get_teachers(self) -> list[dict[str, Any]]:
        response = await self._async_make_http_request(
            url=self.api_url,
            params={"ask": "get_teacher_list"}
        )
        json_data = await response.json()
        return list(json_data["data"].values())

    async def get_teacher_lessons(self, teacher_id: int, semester: str | None = None) -> list[dict[str, Any]]:
        params = {"ask": "get_teacher_schedule", "id": teacher_id}
        if semester is not None:
            params["semester"] = semester
        response = await self._async_make_http_request(
            url=self.api_url,
            params=params
        )
        json_data = await response.json()
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


async def __async_example():
    client = ScheduleUUSTAPIClient(
        api_login="test_login",
        api_password="test_password",
        api_url="https://isu.uust.ru/api/schedule_v2"
    )

    is_conn_good = await client.is_conn_good()
    if is_conn_good:
        print(f"Подключение успешно!")

    try:
        current_week = await client.get_current_week()
        print(f"Текущая неделя: {current_week}")
    except Exception as e:
        print(f"Ошибка получения текущей недели: {e}")

    try:
        current_semester = await client.get_current_semester()
        print(f"Текущий семестр: {current_semester}")
    except Exception as e:
        print(f"Ошибка получения текущего семестра: {e}")

    print("Получаем список групп...")
    try:
        groups = await client.get_groups()
        print(f"Группы: {groups}")
    except Exception as e:
        print(f"Ошибка получения списка групп: {e}")

    if groups:
        group_id = groups[0]["group_id"]
        print(f"Получаем расписание для группы ID {group_id}...")
        try:
            lessons = await client.get_group_lessons(group_id=group_id)
            print(f"Расписание группы {group_id}: {lessons}")
        except Exception as e:
            print(f"Ошибка получения расписания группы: {e}")

    print("Получаем список преподавателей...")
    try:
        teachers = await client.get_teachers()
        print(f"Преподаватели: {teachers}")
    except Exception as e:
        print(f"Ошибка получения списка преподавателей: {e}")

    if teachers:
        teacher_id = teachers[0]["id"]
        print(f"Получаем расписание для преподавателя ID {teacher_id}...")
        try:
            teacher_lessons = await client.get_teacher_lessons(teacher_id=teacher_id)
            print(f"Расписание преподавателя {teacher_id}: {teacher_lessons}")
        except Exception as e:
            print(f"Ошибка получения расписания преподавателя: {e}")


if __name__ == '__main__':
    asyncio.run(__async_example())
