from enum import Enum


class FileStatus(Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class UpdateField(Enum):
    STATUS = "status"
    RESULT = "result"
    PROGRESS = "progress"
