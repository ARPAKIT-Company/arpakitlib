from arpakitlib.ar_json_util import transfer_data_to_json_str


class DictAsObject:
    def __init__(self, data: dict | list):
        self._real_data = data

    def __getattr__(self, item):
        if isinstance(self._real_data, dict):
            try:
                return self.wrap(self._real_data[item])
            except KeyError:
                raise AttributeError(item)

        raise AttributeError(item)

    def __getitem__(self, key):
        if isinstance(self._real_data, (list, dict)):
            return self.wrap(self._real_data[key])
        raise TypeError(f"{type(self._real_data)} is not subscriptable")

    def __len__(self):
        return len(self._real_data)

    def __repr__(self):
        return transfer_data_to_json_str(self._real_data, beautify=True)

    @staticmethod
    def wrap(value):
        if isinstance(value, (dict, list)):
            return DictAsObject(value)
        return value
