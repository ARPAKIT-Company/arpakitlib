# arpakit

from urllib.parse import urlencode, urljoin

from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_arpakit_schedule_uust_site_url(base_url: str = "https://schedule-uust.arpakit.com",
                                            entity_type: str = None,
                                            uust_api_id: int = None,
                                            session: bool = None,
                                            week: int = None,
                                            theme: str = None) -> str:
    if not base_url.endswith("/"):
        base_url += "/"

    params = {}

    if entity_type is not None and entity_type in ["group", "teacher"]: # group/teacher
        raise_for_type(entity_type, str)
        params['entity_type'] = entity_type
    else:
        return base_url

    if uust_api_id is not None:
        raise_for_type(uust_api_id, int)
        params['uust_api_id'] = uust_api_id
    else:
        return base_url

    if session is not None: # false/true
        raise_for_type(session, bool)

        if session:
            params['session'] = "true"
        else:
            params['session'] = "false"
    else:
        params['session'] = "false"

    if week is not None:
        raise_for_type(week, int)
        params['week'] = week
    else:
        return base_url

    if theme is not None and theme in ["dark", "light"]: # dark/light
        raise_for_type(theme, str)
        params['theme'] = theme
    else:
        params['theme'] = "light"


    if params:
        query_string  = urlencode(params)
        result_url = urljoin(base_url, f"schedule?{query_string}")
    else:
        result_url = base_url

    return result_url


def __example():
    base_url = "https://schedule-uust.arpakit.com"
    url = generate_arpakit_schedule_uust_site_url(
        base_url=base_url,
        entity_type="group",
        uust_api_id=6662,
        session=False,
        week=23,
        theme="dark"
    )
    print(url)


if __name__ == '__main__':
    __example()