# arpakit

from __future__ import annotations

import asyncio
import logging
from datetime import timedelta, datetime, time
from typing import Any
from urllib.parse import urljoin

import cachetools
from aiohttp import ClientResponse
from pydantic import ConfigDict, BaseModel

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_http_request_util import async_make_http_request
from arpakitlib.ar_json_util import safely_transfer_obj_to_json_str

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class Weekdays(Enumeration):
    monday = 1
    tuesday = 2
    wednesday = 3
    thursday = 4
    friday = 5
    saturday = 6
    sunday = 7


class Months(Enumeration):
    january = 1
    february = 2
    march = 3
    april = 4
    may = 5
    june = 6
    july = 7
    august = 8
    september = 9
    october = 10
    november = 11
    december = 12


class BaseAPIModel(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)


class CurrentSemesterAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: datetime
    entity_type: str
    actualization_dt: datetime
    value: str


class CurrentWeekAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: datetime
    entity_type: str
    actualization_dt: datetime
    value: int


class GroupAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: datetime
    entity_type: str
    actualization_dt: datetime
    uust_api_id: int
    title: str
    faculty: str | None
    course: int | None
    difference_level: int | None = None
    uust_api_data: dict[str, Any]


class TeacherAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: datetime
    entity_type: str
    actualization_dt: datetime
    uust_api_id: int
    name: str | None
    surname: str | None
    patronymic: str | None
    fullname: str | None
    shortname: str | None
    posts: list[str]
    post: str | None
    units: list[str]
    unit: str | None
    difference_level: int | None
    uust_api_data: dict[str, Any]


class GroupLessonAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: datetime
    entity_type: str
    actualization_dt: datetime
    uust_api_id: int
    type: str
    title: str
    weeks: list[int]
    weekday: int
    comment: str | None
    time_title: str | None
    time_start: time | None
    time_end: time | None
    numbers: list[int]
    location: str | None
    teacher_uust_api_id: int | None
    group_uust_api_id: int | None
    group: GroupAPIModel
    teacher: TeacherAPIModel | None
    uust_api_data: dict[str, Any]

    def compare_type(self, *types: str | list[str]) -> bool:
        type_ = self.type.strip().lower()
        for type__ in types:
            if isinstance(type__, str):
                if type_ == type__.strip().lower():
                    return True
            elif isinstance(type__, list):
                for type___ in type__:
                    if type_ == type___.strip().lower():
                        return True
            else:
                raise TypeError()
        return False


class TeacherLessonAPIModel(BaseAPIModel):
    id: int
    long_id: str
    creation_dt: datetime
    entity_type: str
    actualization_dt: datetime
    uust_api_id: int
    type: str
    title: str
    weeks: list[int]
    weekday: int
    comment: str | None
    time_title: str | None
    time_start: time | None
    time_end: time | None
    numbers: list[int]
    location: str | None
    group_uust_api_ids: list[int]
    teacher_uust_api_id: int
    teacher: TeacherAPIModel
    groups: list[GroupAPIModel]
    uust_api_data: dict[str, Any]

    def compare_type(self, *types: str | list[str]) -> bool:
        type_ = self.type.strip().lower()
        for type__ in types:
            if isinstance(type__, str):
                if type_ == type__.strip().lower():
                    return True
            elif isinstance(type__, list):
                for type___ in type__:
                    if type_ == type___.strip().lower():
                        return True
            else:
                raise TypeError()
        return False


class WeatherInUfaAPIModel(BaseAPIModel):
    temperature: float
    temperature_feels_like: float
    description: str
    wind_speed: float
    sunrise_dt: datetime
    sunset_dt: datetime
    has_rain: bool
    has_snow: bool
    data: dict


class ARPAKITScheduleUUSTAPIClient:
    def __init__(
            self,
            *,
            base_url: str = "https://api.schedule-uust.arpakit.com/api/v1",
            api_key: str | None = "viewer",
            use_cache: bool = False,
            cache_ttl: timedelta | None = timedelta(minutes=10)
    ):
        self._logger = logging.getLogger(__name__)
        self.api_key = api_key
        base_url = base_url.strip()
        if not base_url.endswith("/"):
            base_url += "/"
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key is not None:
            self.headers.update({"apikey": self.api_key})
        self.use_cache = use_cache
        self.cache_ttl = cache_ttl
        if cache_ttl is not None:
            self.ttl_cache = cachetools.TTLCache(maxsize=100, ttl=cache_ttl.total_seconds())
        else:
            self.ttl_cache = None

    def clear_cache(self):
        if self.ttl_cache is not None:
            self.ttl_cache.clear()

    async def _async_make_http_request(
            self,
            *,
            method: str = "GET",
            url: str,
            params: dict[str, Any] | None = None,
            **kwargs
    ) -> ClientResponse:
        response = await async_make_http_request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            raise_for_status_=True,
            **kwargs
        )
        return response

    async def check_auth(self) -> dict[str, Any]:
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "check_auth"))
        json_data = await response.json()
        return json_data

    async def get_current_week(self) -> CurrentWeekAPIModel | None:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_current_week")
        )
        json_data = await response.json()
        if json_data is None:
            return None
        return CurrentWeekAPIModel.model_validate(json_data)

    async def get_current_semester(self) -> CurrentSemesterAPIModel | None:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_current_semester")
        )
        json_data = await response.json()
        if json_data is None:
            return None
        return CurrentSemesterAPIModel.model_validate(json_data)

    async def get_weather_in_ufa(self) -> WeatherInUfaAPIModel:
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_weather_in_ufa")
        )
        json_data = await response.json()
        return WeatherInUfaAPIModel.model_validate(json_data)

    async def get_log_file_content(self) -> str | None:
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "get_log_file"))
        text_data = await response.text()
        return text_data

    async def get_groups(self) -> list[GroupAPIModel]:
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "get_groups"))
        json_data = await response.json()
        return [GroupAPIModel.model_validate(d) for d in json_data]

    async def get_group(
            self, *, filter_id: int | None = None, filter_uust_api_id: int | None = None
    ) -> GroupAPIModel | None:
        params = {}
        if filter_id is not None:
            params["filter_id"] = filter_id
        if filter_uust_api_id is not None:
            params["filter_uust_api_id"] = filter_uust_api_id
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "get_group"),
                                                       params=params)
        json_data = await response.json()
        if json_data is None:
            return None
        return GroupAPIModel.model_validate(json_data)

    async def find_groups(
            self, *, q: str
    ) -> list[GroupAPIModel]:
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "find_groups"),
                                                       params={"q": q.strip()})
        json_data = await response.json()
        return [GroupAPIModel.model_validate(d) for d in json_data]

    async def get_teachers(self) -> list[TeacherAPIModel]:
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "get_teachers"))
        json_data = await response.json()
        return [TeacherAPIModel.model_validate(d) for d in json_data]

    async def get_teacher(
            self, *, filter_id: int | None = None, filter_uust_api_id: int | None = None
    ) -> TeacherAPIModel | None:
        params = {}
        if filter_id is not None:
            params["filter_id"] = filter_id
        if filter_uust_api_id is not None:
            params["filter_uust_api_id"] = filter_uust_api_id
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "get_teacher"),
                                                       params=params)
        json_data = await response.json()
        if json_data is None:
            return None
        return TeacherAPIModel.model_validate(json_data)

    async def find_teachers(
            self, *, q: str
    ) -> list[TeacherAPIModel]:
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "find_teachers"),
                                                       params={"q": q.strip()})
        json_data = await response.json()
        return [TeacherAPIModel.model_validate(d) for d in json_data]

    async def find_any(
            self, *, q: str
    ) -> list[TeacherAPIModel | GroupLessonAPIModel]:
        response = await self._async_make_http_request(method="GET", url=urljoin(self.base_url, "find_any"),
                                                       params={"q": q.strip()})
        json_data = await response.json()

        results = []
        for i in json_data:
            if i.get("entity_type") == "group":
                results.append(GroupAPIModel.model_validate(i))
            elif i.get("entity_type") == "teacher":
                results.append(TeacherAPIModel.model_validate(i))
            else:
                pass
        return results

    async def get_group_lessons(
            self,
            *,
            filter_group_id: int | None = None,
            filter_group_uust_api_id: int | None = None
    ) -> list[GroupLessonAPIModel]:
        params = {}
        if filter_group_id is not None:
            params["filter_group_id"] = filter_group_id
        if filter_group_uust_api_id is not None:
            params["filter_group_uust_api_id"] = filter_group_uust_api_id
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_group_lessons"), params=params
        )
        json_data = await response.json()
        return [GroupLessonAPIModel.model_validate(d) for d in json_data]

    async def get_teacher_lessons(
            self,
            *,
            filter_teacher_id: int | None = None,
            filter_teacher_uust_api_id: int | None = None
    ) -> list[TeacherLessonAPIModel]:
        params = {}
        if filter_teacher_id is not None:
            params["filter_teacher_id"] = filter_teacher_id
        if filter_teacher_uust_api_id is not None:
            params["filter_teacher_uust_api_id"] = filter_teacher_uust_api_id
        response = await self._async_make_http_request(
            method="GET", url=urljoin(self.base_url, "get_teacher_lessons"), params=params
        )
        json_data = await response.json()
        return [TeacherLessonAPIModel.model_validate(d) for d in json_data]


def __example():
    pass


async def __async_example():
    client = ARPAKITScheduleUUSTAPIClient(api_key="viewer", use_cache=True)

    print(f"check_auth")
    print(safely_transfer_obj_to_json_str(await client.check_auth()))

    print(f"get_weather_in_ufa")
    print(safely_transfer_obj_to_json_str((await client.get_weather_in_ufa()).model_dump()))

    print(f"get_current_week")
    print(safely_transfer_obj_to_json_str((await client.get_current_week()).model_dump()))

    print(f"get_current_semester")
    print(safely_transfer_obj_to_json_str((await client.get_current_semester()).model_dump()))

    # Group
    print(f"get_groups")
    print(safely_transfer_obj_to_json_str((await client.get_groups())))

    print(f"get_group")
    if await client.get_group(filter_id=25285, filter_uust_api_id=6674):
        print(safely_transfer_obj_to_json_str(
            (await client.get_group(filter_id=25285, filter_uust_api_id=6674)).model_dump()))
    else:
        print("Group is none")

    print(f"find_groups")
    print(safely_transfer_obj_to_json_str((await client.find_groups(q="ПИ-427Б"))))

    # Teacher
    print(f"get_teachers")
    print(safely_transfer_obj_to_json_str((await client.get_teachers())))

    print(f"get_teacher")
    if await client.get_teacher(filter_id=16975, filter_uust_api_id=112978):
        print(safely_transfer_obj_to_json_str(
            (await client.get_teacher(filter_id=16975, filter_uust_api_id=112978)).model_dump()))
    else:
        print("Teacher is none")

    print(f"find_teachers")
    print(safely_transfer_obj_to_json_str((await client.find_teachers(q="Казанцев"))))

    # Group Lesson
    print(f"get_group_lessons")
    if await client.get_group_lessons(filter_group_id=25285, filter_group_uust_api_id=6674):
        print(safely_transfer_obj_to_json_str((await client.get_group_lessons(filter_group_id=25285,
                                                                              filter_group_uust_api_id=6674))))
    else:
        print("Group lessons is none")

    # Teacher Lesson
    print(f"get_teacher_lessons")
    if await client.get_teacher_lessons(filter_teacher_id=16975, filter_teacher_uust_api_id=112978):
        print(safely_transfer_obj_to_json_str((await client.get_teacher_lessons(filter_teacher_id=16975,
                                                                                filter_teacher_uust_api_id=112978))))
    else:
        print("Teacher lessons is none")

    # Find Any
    print(f"find_any")
    print(safely_transfer_obj_to_json_str((await client.find_any(q="ПИ"))))


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
