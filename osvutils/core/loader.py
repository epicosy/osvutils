
from typing import List
from pathlib import Path

from osvutils.utils.misc import load_osv_file, get_ecosystems
from osvutils.types.osv import OSV


class OSVDataLoader:
    def __init__(self, data_path: str = '~/.osvutils/gs', verbose: bool = False):
        self.data_path = Path(data_path).expanduser()
        self.verbose = verbose

        # check if the data path exists
        if not self.data_path.exists():
            raise FileNotFoundError(f"{self.data_path} not found")

        self.records = {}

    def __iter__(self):
        """
        Makes the loader iterable over the records.
        """
        return iter(self.records.items())

    def __len__(self):
        return sum([len(v) for v in self.records.values()])

    def __call__(self, ecosystems: list = None):
        """
            Main entry point for loading the OSV records.
        """

        for ecosystem in get_ecosystems(ecosystems):
            self._process_ecosystem(ecosystem.value)

    def _process_ecosystem(self, ecosystem: str):
        ecosystem_files = self.get_ecosystem_files(ecosystem)

        if ecosystem_files:
            if ecosystem not in self.records:
                self.records[ecosystem] = {}

            for file in ecosystem_files:
                if file.suffix != '.json':
                    continue

                if file.stem not in self.records[ecosystem]:
                    osv_data = load_osv_file(file)
                    self.records[ecosystem][file.stem] = OSV(**osv_data)

    def get_ecosystem_files(self, ecosystem: str) -> List[Path]:
        ecosystem_path = self.data_path / ecosystem

        if ecosystem_path.exists():
            print(f"Loading {ecosystem} data...")
            return list(ecosystem_path.iterdir())

        if self.verbose:
            print(f"{ecosystem_path} not found")

        return []
