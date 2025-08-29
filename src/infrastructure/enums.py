import enum


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
