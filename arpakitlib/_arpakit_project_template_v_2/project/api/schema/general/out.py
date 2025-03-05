from project.api.schema.base_schema import BaseSO


class BaseGeneralSO(BaseSO):
    pass


class HealthcheckGeneralSO(BaseGeneralSO):
    is_ok: bool = True


class ErrorsInfoGeneralSO(BaseGeneralSO):
    api_error_codes: list[str] = []
    api_error_specification_codes: list[str] = []
