# =========================================================
# FILE: app/utils/constants.py
# =========================================================

"""
=========================================================
SYSTEM CONSTANTS
=========================================================
- Chứa toàn bộ constant hệ thống
- Tránh hard-code string
- Dễ maintain
=========================================================
"""

# =========================================================
# SYSTEM INFO
# =========================================================
SYSTEM_NAME = "Smart Document Management System"

SYSTEM_VERSION = "1.0.0"

DEFAULT_AVATAR = "default.png"


# =========================================================
# USER ROLES
# =========================================================
ROLE_ADMIN = "admin"

ROLE_STAFF = "staff"

ROLE_EMPLOYEE = "employee"


# =========================================================
# USER STATUS
# =========================================================
USER_ACTIVE = 1

USER_INACTIVE = 0


# =========================================================
# DOCUMENT STATUS
# =========================================================
STATUS_PENDING = "pending"

STATUS_PROCESSING = "processing"

STATUS_APPROVED = "approved"

STATUS_REJECTED = "rejected"

STATUS_COMPLETED = "completed"


# =========================================================
# DOCUMENT PRIORITY
# =========================================================
PRIORITY_LOW = "low"

PRIORITY_NORMAL = "normal"

PRIORITY_HIGH = "high"

PRIORITY_URGENT = "urgent"


# =========================================================
# DOCUMENT TYPES
# =========================================================
DOC_TYPE_INCOMING = "incoming"

DOC_TYPE_OUTGOING = "outgoing"

DOC_TYPE_INTERNAL = "internal"


# =========================================================
# ALLOWED FILE EXTENSIONS
# =========================================================
ALLOWED_EXTENSIONS = {
    'pdf',
    'doc',
    'docx',
    'xls',
    'xlsx',
    'png',
    'jpg',
    'jpeg'
}


# =========================================================
# PAGINATION
# =========================================================
DEFAULT_PAGE_SIZE = 10

MAX_PAGE_SIZE = 100