
from tqdm import tqdm
from pathlib import Path
from typing import List, Dict

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

        for ecosystem in tqdm(get_ecosystems(ecosystems), desc="Loading ecosystems"):
            self._process_ecosystem(ecosystem.value)

    def _process_ecosystem(self, ecosystem: str):
        ecosystem_files = self.get_ecosystem_files(ecosystem)

        if ecosystem_files:
            if ecosystem not in self.records:
                self.records[ecosystem] = {}

            for file in tqdm(ecosystem_files, desc=f"Loading {ecosystem} entries", leave=False):
                if file.suffix != '.json':
                    continue

                if file.stem not in self.records[ecosystem]:
                    osv_data = load_osv_file(file)
                    self.records[ecosystem][file.stem] = OSV(**osv_data)

    def get_ecosystem_files(self, ecosystem: str) -> List[Path]:
        ecosystem_path = self.data_path / ecosystem

        if ecosystem_path.exists():
            return list(ecosystem_path.iterdir())

        if self.verbose:
            print(f"{ecosystem_path} not found")

        return []

    def get_osv_with_cve_ids(self, ecosystems: List[str] = None, has_fix_refs: bool = False) -> Dict[str, OSV]:
        """
            Get all the OSV records that have CVE aliases or CVE IDs.

        :param ecosystems: List of ecosystems to filter the records by.
        :param has_fix_refs: When True, includes only the records that have fix references.

        :return:
        """
        # TODO: add this as an option, so it performs the filtering on when the records are loaded
        cve_ids = {}

        for ecosystem, records in tqdm(self.records.items()):
            if ecosystems and ecosystem not in ecosystems:
                continue

            for record in records.values():
                cve_id = record.get_cve_id()

                if cve_id is not None:
                    if has_fix_refs and not record.has_fix_refs():
                        continue

                    cve_ids[cve_id] = record

        return cve_ids
