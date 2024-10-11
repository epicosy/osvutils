import re
import json

from typing import List
from pathlib import Path

from osvutils.types.alias import AliasType
from osvutils.types.ecosystem import EcosystemType

CVE_REGEX = r'CVE-\d{4}-\d{4,7}'


def load_osv_file(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")
    if path.suffix != '.json':
        raise ValueError(f"{path} is not a json file")
    if path.stat().st_size == 0:
        raise ValueError(f"{path} is empty")

    # read contents of the file
    with path.open('r') as f:
        osv_data = json.load(f)

    return osv_data


def get_ecosystems(ecosystems: list = None) -> List[EcosystemType]:
    ecosystem_list = []
    ecosystem_types = [ecosystem.value for ecosystem in EcosystemType]

    if ecosystems:
        for ecosystem in ecosystems:
            if ecosystem not in ecosystem_types:
                print(f"Invalid ecosystem: {ecosystem}")
                continue

            ecosystem_list.append(EcosystemType(ecosystem))

        if not ecosystem_list:
            print("No valid ecosystems found")
    else:
        ecosystem_list = list(EcosystemType)

    return ecosystem_list


def get_alias_type(value: str) -> AliasType:
    if re.search(CVE_REGEX, value):
        return AliasType.CVE

    return AliasType.Other


def is_cve_id(value: str) -> bool:
    return re.search(CVE_REGEX, value) is not None


def get_cve_match(value: str) -> str | None:
    match = re.search(CVE_REGEX, value)
    return match.group() if match else None
