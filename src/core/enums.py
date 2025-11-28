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


class WorkScheduleType(enum.Enum):
    ONE_BY_ONE = "1/1"
    ONE_BY_TWO = "1/2"
    TWO_BY_TWO = "2/2"
    THREE_BY_TWO = "3/2"
    THREE_BY_THREE = "3/3"
    FOUR_BY_TWO = "4/2"
    FOUR_BY_THREE = "4/3"
    FOUR_BY_FOUR = "4/4"
    FIVE_BY_TWO = "5/2"
    SIX_BY_ONE = "6/1"
    ON_WEEKENDS = "on weekends"
    FLEXIBLE = "flexible schedule"
    OTHER = "other schedule"


class Currency(enum.Enum):
    USD = "USD"
    EUR = "EUR"
    RUB = "RUB"
    BYN = "BYN"


class VacancyDuration(enum.Enum):
    WEEK = "7"
    TWO_WEEKS = "14"
    MONTH = "30"
    THREE_MONTH = "90"
    SIX_MONTH = "180"


class StatusRespond(enum.Enum):
    """
    Enums of respond of vacancy by applicant or company on resume.
    SENT - applicant/company sent responded
    VIEWED - applicant/company viewed the response
    ACCEPTED - applicant/company accepted the response
    DECLINED - applicant/company the response
    PENDING - applicant/company will be to think about response
    """

    SENT = "SENT"
    VIEWED = "VIEWED"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    PENDING = "PENDING"


class ActorType(enum.Enum):
    APPLICANT = "APPLICANT"
    COMPANY = "COMPANY"
