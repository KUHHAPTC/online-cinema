import enum


class Role(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class MovieRole(enum.Enum):
    LEAD = "lead"
    SUPPORT = "support"
    EPISODE = "episode"
    CAMEO = "cameo"
    UNMENTIONED = "unmentioned"
