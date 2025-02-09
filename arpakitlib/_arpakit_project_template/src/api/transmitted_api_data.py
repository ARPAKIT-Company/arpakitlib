from arpakitlib.ar_fastapi_util import AdvancedTransmittedAPIData

from src.core.settings import Settings


class TransmittedAPIData(AdvancedTransmittedAPIData):
    settings: Settings | None = None
