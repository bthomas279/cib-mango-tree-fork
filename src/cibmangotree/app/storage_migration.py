from enum import Enum
from pathlib import Path


class StorageMigrationStatus(Enum):
    NOT_FOUND = "not_found"
    MOVED = "moved"
    CONFLICT = "conflict"
    ERROR = "error"


def storage_directory_migration(old: Path, new: Path) -> StorageMigrationStatus:
    if not old.exists():
        return StorageMigrationStatus.NOT_FOUND

    if new.exists():
        if any(new.iterdir()):
            return StorageMigrationStatus.CONFLICT
        new.rmdir()

    # Move
    try:
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)

    except OSError:
        return StorageMigrationStatus.ERROR

    return StorageMigrationStatus.MOVED
