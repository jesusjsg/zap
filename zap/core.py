from collections.abc import Generator
from pathlib import Path
from .utils import validate_extension

FILE_TYPES = {
    "Documents": ["docx", "doc", "pdf", "xlsx", "xls", "pptx", "ppt"],
    "Music": ["mp3", "wav", "flac", "m4a", "wma", "ogg"],
    "Pictures": ["png", "jpg", "jpeg", "gif", "bmp", "webp"],
}


def list_files(
    path: Path, ext: str | None, long: bool, printer
) -> Generator[tuple[str, str], None, None]:
    for file in sorted(path.iterdir()):
        if file.is_dir() and ext:
            continue
        if file.is_file() and not validate_extension(file, ext):
            continue
        name, color = printer(file, long)
        yield name, color


def delete_files(path: Path, ext: str | None) -> str:
    count = 0
    if ext:
        for file in path.iterdir():
            if file.is_file() and not validate_extension(file, ext):
                file.unlink()
                count += 1
        return f"Zapped files with extension {ext}"
    else:
        for file in path.iterdir():
            if file.is_file():
                file.unlink()
                count += 1
        path.rmdir()
        return f"Zapped dir {path.name}"


def clean_and_move_files(path: Path, ext: str | None) -> list[str]:
    home_path = Path.home()
    moved_files = []

    files = [
        file
        for file in path.iterdir()
        if file.is_file() and validate_extension(file, ext)
    ]

    for file in files:
        extension = file.suffix.lower().lstrip(".")
        destination_path = None
        for folder, extensions in FILE_TYPES.items():
            if extension in extensions:
                destination_path = home_path.joinpath(folder)
                break
        if not destination_path:
            continue

        destination_path.mkdir(parents=True, exist_ok=True)
        destination = destination_path.joinpath(file.name)

        if destination.exists():
            moved_files.append(
                f"Skipping {file.name} because it already exists"
            )
            continue

        file.rename(destination)
        moved_files.append(f"Moved {file.name} to {destination_path.name}")
    return moved_files
