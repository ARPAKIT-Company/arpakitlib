import os

from arpakitlib.ar_json_db_util import BaseJSONDb


class JSONDb(BaseJSONDb):
    def __init__(self, dirpath: str):
        super().__init__()
        self.story_log = self.create_json_db_file(
            filepath=os.path.join(dirpath, "story_log.json"), use_memory=True, beautify_json=False
        )
