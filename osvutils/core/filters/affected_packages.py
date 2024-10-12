from dataclasses import dataclass

from osvutils.core.filters.base import FilterCheck, BaseFilter, OptionCheck
from osvutils.types.osv import OSV


@dataclass
class AffectedPackagesFilter(BaseFilter):
    """
        Class to store options for filtering entries by using affected fields

        Attributes:
            has_git_ranges (bool): Whether to filter out entries with git ranges
    """
    has_git_ranges: bool = False

    def check(self, entry: OSV) -> FilterCheck:
        filter_check = FilterCheck()
        filter_check.update('has_git_ranges', OptionCheck(self.has_git_ranges, entry.has_git_ranges()))

        return filter_check
