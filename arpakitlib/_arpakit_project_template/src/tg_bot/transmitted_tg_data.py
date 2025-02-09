from arpakitlib.ar_aiogram_util import AdvancedTransmittedTgBotData
from src.core.settings import Settings


class TransmittedTgData(AdvancedTransmittedTgBotData):
    settings: Settings | None = None
