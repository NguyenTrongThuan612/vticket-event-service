from enum import Enum

class InstanceErrorEnum(Enum):
    ALL_OK = "ALL_OK"
    EXISTED = "EXISTED"
    NOT_EXISTED = "NOT_EXISTED"
    DELETED = "DELETED"
    EXCEPTION = "EXCEPTION"