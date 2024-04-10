from dataclasses import dataclass, field
import datetime

from vticket_app.enums.role_enum import RoleEnum
from vticket_app.enums.gender_enum import GenderEnum
from vticket_app.enums.account_status_enum import AccountStatusEnum

@dataclass
class UserDTO():
    id: int = None
    email: str = None
    first_name: str = None
    last_name: str = None
    gender: GenderEnum = None
    birthday: datetime.date = None
    avatar_url: str = None
    phone_number: str = None
    status: AccountStatusEnum = None
    role: RoleEnum = None
    last_login: datetime.datetime = None

    def __post_init__(self):
        self.gender = (GenderEnum)(self.gender)
        self.status = (AccountStatusEnum)(self.status)
        self.role = (RoleEnum)(self.role)