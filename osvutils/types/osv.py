from datetime import datetime
from pydantic import BaseModel, field_validator, Field
from typing import List, Optional

from osvutils.types.package import Package
from osvutils.types.alias import Alias
from osvutils.types.reference import Reference
from osvutils.utils.misc import get_alias_type, is_cve_id, get_cve_match


# Severity model
class Severity(BaseModel):
    type: str
    score: str


# Event model
class Event(BaseModel):
    introduced: Optional[str] = None
    fixed: Optional[str] = None
    last_affected: Optional[str] = None
    limit: Optional[str] = None


# Range model
class Range(BaseModel):
    type: str
    events: List[Event]
    repo: Optional[str] = None
    database_specific: Optional[dict] = None  # Adjust according to your needs


# Affected model
class Affected(BaseModel):
    package: Optional[Package] = None
    severity: Optional[List[Severity]] = None
    ranges: Optional[List[Range]] = None
    versions: Optional[List[str]] = None
    ecosystem_specific: Optional[dict] = None  # Adjust according to your needs
    database_specific: Optional[dict] = None  # Adjust according to your needs


# Credit model
class Credit(BaseModel):
    name: str
    contact: Optional[List[str]] = None
    type: str


# Main schema model: version 1.6.0
# TODO: implement other schema versions
class OSV(BaseModel):
    schema_version: str
    id: str
    modified: datetime
    published: datetime
    withdrawn: Optional[str] = None
    aliases: Optional[List[Alias]] = None
    related: Optional[List[str]] = None
    summary: Optional[str] = None
    details: Optional[str] = None
    severity: Optional[List[Severity]] = None
    affected: Optional[List[Affected]] = None
    references: Optional[List[Reference]] = Field(
        default=None,
        description="List of reference objects or None"
    )
    credits: Optional[List[Credit]] = None
    database_specific: Optional[dict] = None  # TODO: to be extended for each database

    @field_validator('aliases', mode='before')
    def parse_aliases(cls, v: List[str]):
        if isinstance(v, list):
            # If v is a list, we assume it's already in the correct format
            return [Alias(type=get_alias_type(alias), value=alias) for alias in v]

        return []

    def has_aliases(self) -> bool:
        return self.aliases and len(self.aliases) > 0

    def has_cve_id(self) -> bool:
        if self.has_aliases():
            return any(alias.is_cve() for alias in self.aliases)

        return False

    def is_cve_id(self) -> bool:
        return is_cve_id(self.id)

    def get_cve_id(self) -> Optional[str]:
        # TODO: temporary solution, there should be a flag or variable to indicate/store the matched cve_id
        cve_id = get_cve_match(self.id)

        if cve_id:
            return cve_id

        if self.has_aliases():
            for alias in self.aliases:
                if alias.is_cve():
                    return alias.value

        return None

    def has_references(self) -> bool:
        return self.references and len(self.references) > 0

    def has_fix_refs(self) -> bool:
        if self.has_references():
            return any(ref.is_fix() for ref in self.references)

        return False
