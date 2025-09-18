import enum


class TypeUser(enum.Enum):
    APPLICANT = "applicant"
    COMPANY = "company"


class GenderEnum(enum.Enum):
    MALE = "male"
    FEMALE = "female"


class EducationEnum(enum.Enum):
    WITHOUT_EDUCATION = "without_education"
    SECONDARY_SPECIAL = "secondary_special"
    INCOMPLETE_HIGHER = "incomplete_higher"
    HIGHER = "higher"
    BACHELOR = "bachelor"
    MASTER = "master"
    PHD = "phd"
    DOCTOR_SCIENCE = "doctor_science"


class EmploymentType(enum.Enum):
    FULL_TIME = "full time"
    PART_TIME = "part time"
    REMOTE = "remote work"
    FLEX = "flex work"
    SHIFT_WORK = "shift work"
    FREELANCE = "freelance"


class Currency(enum.Enum):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"
    BYN = "BYN"

