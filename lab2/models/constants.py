from enum import StrEnum


class ColumnState(StrEnum):
    STANDING = "standing"
    DESTROYED = "destroyed"


class BirdState(StrEnum):
    LOOKING_FOR_COLUMN = "looking_for_column"
    FLYING_TO_COLUMN = "fly_to_column"
    SITTING = "sitting"
    FLYING_AWAY = "flying_away"
    FLEW_AWAY = "flew_away"
