from pathlib import Path
from datetime import datetime


def validate_extension(file: Path, ext: str | None) -> bool:
    if ext is None:
        return True
    return file.suffix.lower() == ext.lower()


def get_file_info(file: Path) -> tuple[int, str, str, str, str]:
    size = file.stat().st_size
    user = file.owner()
    group = file.group()
    date = datetime.fromtimestamp(file.stat().st_mtime).strftime(
        "%b-%d-%Y %H:%M"
    )
    name = file.name
    return size, user, group, date, name


def validate_path(path: Path) -> bool:
    if not path.exists():
        return False
    return True
