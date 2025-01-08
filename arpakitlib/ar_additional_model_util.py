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
    class UserModel(BaseAM):
        id: int
        name: str
        email: str

    user = UserModel(id=1, name="John Doe", email="john.doe@example.com")
    print(user.name)  # John Doe

    # bus_data
    user.bus_data["age"] = 22
    print(user.bus_data)  # {'age': '22'}


if __name__ == '__main__':
    __example()
