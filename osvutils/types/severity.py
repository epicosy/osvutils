import re

from enum import Enum
from pydantic import BaseModel, model_validator

from osvutils.utils.patterns import CVSS_V2_PATTERN, CVSS_V3_PATTERN, CVSS_V4_PATTERN


# Enum for the severity types
class SeverityType(str, Enum):
    CVSS_V2 = 'CVSS_V2'
    CVSS_V3 = 'CVSS_V3'
    CVSS_V4 = 'CVSS_V4'


# Severity model
class Severity(BaseModel):
    type: SeverityType
    score: str

    @model_validator(mode='before')
    def validate_severity(cls, values):
        severity_type = values.get('type')
        score = values.get('score')

        if severity_type == SeverityType.CVSS_V2:
            pattern = CVSS_V2_PATTERN
        elif severity_type == SeverityType.CVSS_V3:
            pattern = CVSS_V3_PATTERN
        elif severity_type == SeverityType.CVSS_V4:
            pattern = CVSS_V4_PATTERN
        else:
            raise ValueError(f"Unknown severity type: {severity_type}")

        # Validate score based on the pattern for the given severity type
        if not re.match(pattern, score):
            raise ValueError(f"Invalid score format for {severity_type}. Given score: {score}")

        return values
