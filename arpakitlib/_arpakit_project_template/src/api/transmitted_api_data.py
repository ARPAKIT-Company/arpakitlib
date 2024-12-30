from arpakitlib.ar_fastapi_util import BaseTransmittedAPIData
from arpakitlib.ar_sqlalchemy_util import SQLAlchemyDB

from src.core.settings import Settings


class TransmittedAPIData(BaseTransmittedAPIData):
    settings: Settings
    sqlalchemy_db: SQLAlchemyDB | None = None
