from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, model_validator


from osvutils.types.event import Event, event_mapping, Fixed, LastAffected


class RangeType(str, Enum):
    GIT = 'GIT'
    SEMVER = 'SEMVER'
    ECOSYSTEM = 'ECOSYSTEM'


# Range model with all properties and conditional validation
class Range(BaseModel):
    type: RangeType
    events: List[Event]
    database_specific: Optional[dict] = None  # TODO: to be extended for each database

    @model_validator(mode='before')
    def validate_events(cls, values):
        events = values.get('events', [])

        if not any(events):
            raise ValueError("At least one of 'introduced', 'fixed', 'last_affected', or 'limit' must be provided")

        processed_events = []

        # Ensure that the type matches the expected event types
        for event in events:
            if len(event) != 1:
                raise ValueError("Only one event type is allowed per event object")

            for event_type, version in event.items():
                if event_type not in event_mapping:
                    raise ValueError(f"Invalid event type: {event_type}")

                processed_events.append(event_mapping[event_type](version=version))

        # Replace the original 'events' data with the processed list of objects
        values['events'] = processed_events

        return values


class GitRange(Range):
    repo: str

    # Conditional logic for GIT type requiring repo
    @model_validator(mode='before')
    def check_git_repo(cls, values):
        if values.get('type') == 'GIT' and not values.get('repo'):
            raise ValueError("GIT ranges require a 'repo' field.")
        return values

    # TODO: the schema indicates that 'fixed' and 'last_affected' are required and mutually exclusive but some entries
    #  do not follow this rule. Uncomment the following code to enforce this rule.
    # @model_validator(mode='after')
    # def validate_git_events(cls, values):
    #     # Check if both 'fixed' and 'last_affected' are present
    #     fixed_events = [e for e in values.events if isinstance(e, Fixed)]
    #     last_affected_events = [e for e in values.events if isinstance(e, LastAffected)]
    #
    #     # Check for mutual exclusivity
    #     if fixed_events and last_affected_events:
    #         raise ValueError("'fixed' and 'last_affected' events must have different versions.")
    #
    #     # At least one of 'fixed' or 'last_affected' must be present
    #     if not fixed_events and not last_affected_events:
    #         raise ValueError("Either 'fixed' or 'last_affected' event is required.")
    #
    #     return values
