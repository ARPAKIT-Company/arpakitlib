# arpakit
import asyncio
import logging
import time
from datetime import timedelta, datetime
from typing import Any, Optional, Self, Iterator

from pyzabbix import ZabbixAPI

from arpakitlib.ar_list_util import iter_group_list
from arpakitlib.ar_logging_util import setup_normal_logging
from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class ZabbixApiClient:

    def __init__(
            self,
            *,
            api_url: str,
            api_user: str,
            api_password: str,
            timeout: float | int | timedelta = timedelta(seconds=15).total_seconds()
    ):
        self._logger = logging.getLogger(self.__class__.__name__)

        raise_for_type(api_url, str)
        self.api_url = api_url

        raise_for_type(api_user, str)
        self.api_user = api_user

        raise_for_type(api_password, str)
        self.api_password = api_password

        if isinstance(timeout, float):
            timeout = timedelta(timeout)
        elif isinstance(timeout, int):
            timeout = timedelta(timeout)
        elif isinstance(timeout, timedelta):
            pass
        else:
            raise_for_type(timeout, timedelta)

        self.zabbix_api = ZabbixAPI(
            server=self.api_url,
            timeout=timeout.total_seconds(),
        )
        self.zabbix_api.session.verify = False

        self.is_logged_in = False

    def login(self) -> Self:
        self.zabbix_api.login(user=self.api_user, password=self.api_password)
        self.is_logged_in = True
        return self

    def login_if_not_logged_in(self):
        if not self.is_logged_in:
            self.login()
        return self

    def is_login_good(self) -> bool:
        try:
            self.login()
        except Exception as e:
            self._logger.error(e)
            return False
        return True

    def get_host_ids(self) -> list[str]:
        kwargs = {"output": ["hostid"]}
        self.login_if_not_logged_in()
        host_ids = self.zabbix_api.host.get(**kwargs)
        kwargs["sortfield"] = "hostid"
        kwargs["sortorder"] = "DESC"
        return [host_id["hostid"] for host_id in host_ids]

    def get_hosts(self, *, host_ids: Optional[list[str | int]] = None) -> list[dict[str, Any]]:
        kwargs = {
            "output": "extend",
            "selectInterfaces": "extend",
            "selectInventory": "extend",
            "selectMacros": "extend",
            "selectGroups": "extend"
        }
        if host_ids is not None:
            kwargs["hostids"] = host_ids
        kwargs["sortfield"] = "hostid"
        kwargs["sortorder"] = "DESC"

        self.login_if_not_logged_in()
        hosts = self.zabbix_api.host.get(**kwargs)
        for d in hosts:
            d["hostid_int"] = int(d["hostid"])

        return hosts

    def iter_all_hosts(self) -> Iterator[list[dict[str, Any]]]:
        host_ids = self.login_if_not_logged_in().get_host_ids()
        for zabbix_api_host_ids in iter_group_list(list_=host_ids, n=100):
            hosts = self.get_hosts(host_ids=zabbix_api_host_ids)
            yield hosts

    def iter_all_hosts_by_one(self) -> Iterator[dict[str, Any]]:
        for hosts in self.iter_all_hosts():
            for host in hosts:
                yield host

    def get_all_hosts(self) -> list[dict[str, Any]]:
        res = []
        for hosts in self.iter_all_hosts():
            res += hosts
        return res

    def get_item_ids(
            self,
            *,
            host_ids: Optional[list[str | int]] = None,
            keys: Optional[list[str]] = None,
            names: Optional[list[str]] = None,
            limit: Optional[int] = None
    ) -> list[str]:
        kwargs = {"output": ["itemid"]}
        if host_ids is not None:
            kwargs["hostids"] = host_ids
        if keys is not None:
            if "filter" not in kwargs.keys():
                kwargs["filter"] = {}
            if "key_" not in kwargs["filter"].keys():
                kwargs["filter"]["key_"] = []
            kwargs["filter"]["key_"] = keys
        if names is not None:
            if "filter" not in kwargs.keys():
                kwargs["filter"] = {}
            if "name" not in kwargs["filter"].keys():
                kwargs["filter"]["name"] = []
            kwargs["filter"]["name"] = names
        if limit is not None:
            kwargs["limit"] = limit
        kwargs["sortfield"] = "itemid"
        kwargs["sortorder"] = "DESC"
        self.login_if_not_logged_in()
        itemid_ids = self.zabbix_api.item.get(**kwargs)
        res = [d["itemid"] for d in itemid_ids]
        return res

    def get_items(
            self,
            *,
            host_ids: Optional[list[str | int]] = None,
            item_ids: Optional[list[str | int]] = None,
            keys: Optional[list[str]] = None,
            names: Optional[list[str]] = None,
            limit: Optional[int] = None
    ) -> list[dict[str, Any]]:
        kwargs = {
            "output": "extend",
            "selectInterfaces": "extend"
        }
        if host_ids is not None:
            kwargs["hostids"] = host_ids
        if item_ids is not None:
            kwargs["itemids"] = item_ids
        if keys is not None:
            if "filter" not in kwargs.keys():
                kwargs["filter"] = {}
            if "key_" not in kwargs["filter"].keys():
                kwargs["filter"]["key_"] = []
            kwargs["filter"]["key_"] = keys
        if names is not None:
            if "filter" not in kwargs.keys():
                kwargs["filter"] = {}
            if "name" not in kwargs["filter"].keys():
                kwargs["filter"]["name"] = []
            kwargs["filter"]["name"] = names
        if limit is not None:
            kwargs["limit"] = limit
        kwargs["sortfield"] = "itemid"
        kwargs["sortorder"] = "DESC"
        self.login_if_not_logged_in()
        res = self.zabbix_api.item.get(**kwargs)
        for d in res:
            d["itemid_int"] = int(d["itemid"])
            d["hostid_int"] = int(d["hostid"])
        return res

    def iter_all_items(
            self,
            *,
            host_ids: Optional[list[str | int]] = None,
            keys: Optional[list[str]] = None,
            names: Optional[list[str]] = None
    ) -> Iterator[list[dict[str, Any]]]:
        item_ids = self.get_item_ids(
            host_ids=host_ids,
            keys=keys,
            names=names
        )
        for item_ids_ in iter_group_list(item_ids, n=100):
            yield self.get_items(item_ids=item_ids_)

    def iter_all_items_by_one(
            self,
            *,
            host_ids: Optional[list[str | int]] = None,
            keys: Optional[list[str]] = None,
            names: Optional[list[str]] = None
    ) -> Iterator[dict[str, Any]]:
        for items in self.iter_all_items(host_ids=host_ids, keys=keys, names=names):
            for item in items:
                yield item

    def get_all_items(
            self,
            *,
            host_ids: list[str | int] | None = None,
            keys: list[str] | None = None,
            names: list[str] | None = None
    ) -> list[dict[str, Any]]:
        return [
            item
            for item in self.iter_all_items_by_one(host_ids=host_ids, keys=keys, names=names)
        ]

    def get_histories(
            self,
            *,
            host_ids: Optional[list[str | int]] = None,
            item_ids: Optional[list[str | int]] = None,
            limit: Optional[int] = None,
            history: int = 0,
            time_from: Optional[datetime] = None,
            time_till: Optional[datetime] = None
    ) -> list[dict[str, Any]]:
        kwargs = {
            "output": "extend"
        }
        if host_ids is not None:
            kwargs["hostids"] = host_ids
        if item_ids is not None:
            kwargs["itemids"] = item_ids
        if limit is not None:
            kwargs["limit"] = limit
        if history is not None:
            kwargs["history"] = history
        if time_from is not None:
            kwargs["time_from"] = int(time.mktime((
                time_from.year, time_from.month, time_from.day, time_from.hour, time_from.minute, time_from.second, 0,
                0, 0
            )))
        if time_till is not None:
            kwargs["time_till"] = int(time.mktime((
                time_till.year, time_till.month, time_till.day, time_till.hour, time_till.minute, time_till.second, 0,
                0, 0
            )))

        self.login_if_not_logged_in()
        histories: list[dict[str, Any]] = self.zabbix_api.history.get(**kwargs)

        for history in histories:
            if "clock" in history.keys():
                clock_ns_as_datetime = datetime.fromtimestamp(int(history["clock"]))
                if "ns" in history.keys():
                    clock_ns_as_datetime += timedelta(microseconds=int(history["ns"]) / 1000)
                    history["dt"] = clock_ns_as_datetime
                    history["assembled_key"] = (
                        f"{history["clock"]}_{history["ns"]}_{history["value"]}_{history["itemid"]}"
                    )

        return histories


ZabbixAPIClient = ZabbixApiClient


def __example():
    setup_normal_logging()


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
