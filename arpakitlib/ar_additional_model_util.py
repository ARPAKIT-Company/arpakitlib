# arpakit
from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseAM(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)
    _bus_data: dict[str, Any] | None = None

    @property
    def bus_data(self) -> dict[str, Any]:
        if self._bus_data is None:
            self._bus_data = {}
        return self._bus_data


def __example():
    pass


if __name__ == '__main__':
    __example()
