from enum import Enum

class RestResponseStatusEnum(Enum):
    DEFINED_ERROR = (0, "Lỗi!")
    SUCCESS = (1, "Thành công")
    PERMISSION_DENIED = (2, "Rất tiếc! Bạn không có quyền truy cập tài nguyên này!")
    UNAUTHENTICATED = (3, "Uh oh! Bạn cần phải đăng nhập trước khi tiếp tục phiêu lưu.")
    THROTTLED = (4, "Oops! Sống chậm lai nào bạn ơi.")
    VALIDATION_FAILED = (5, "Pipppp! Dữ liệu này... trông hơi mờ ám!")
    INTERNAL_SERVER_ERROR = (6, "Oops! Máy chủ của chúng tôi đang chịu ảnh hưởng bởi một lực lượng siêu nhiên. Hãy kiên nhẫn chờ đợi trong khi chúng tôi triệu hồi thần linh sửa chữa!")
    DIRECT = (7, "")
    INVALID_TOKEN = (8, "Invalid token!")