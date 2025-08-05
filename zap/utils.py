from pathlib import Path
from datetime import datetime


def validate_extension(file: Path, ext: str | None) -> bool:
    return True if ext is None else file.suffix.lower() == ext.lower()


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
    return True if path.exists() else False


def print_output(file: Path, long: bool = False) -> tuple[str, str]:
    if long:
        size, user, group, date, name = get_file_info(file)
        formated_line = f"{name:<20} {size:<10} {user:<10} {group:<10} {date}"
        return formated_line, "cyan"
    name = f"{file.name}" if file.is_dir() else file.name
    color = "blue" if file.is_dir() else "green"
    return name, color
