import click
from pathlib import Path
from datetime import datetime


def _validate_extension(file: Path, ext: str | None) -> bool:
    if ext is None:
        return True
    return file.suffix.lower() == ext.lower()


def _get_file_info(file: Path) -> tuple[int, str, str]:
    size = file.stat().st_size
    date = datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    name = file.name
    return size, date, name


def _print_output(file: Path, long: bool = False) -> None:
    if long:
        size, date, name = _get_file_info(file)
        click.secho(f"{size}\t {date}\t", nl=False)
    name = f"{file.name}" if file.is_dir() else file.name
    color = "blue" if file.is_dir() else "green"
    click.secho(name, fg=color)


@click.group()
def cli():
    """Zap is a tool to say goodbye to your files"""
    pass


@cli.command()
@click.option("-e", "--ext", type=click.STRING, help="Listing files with extension")
@click.option("-l", "--long", is_flag=True, help="Long listing")
@click.argument("dir", type=click.Path(exists=True, path_type=Path), default=".")
def zl(dir: Path, ext: str | None, long: bool) -> None:
    """List current directory files"""
    if not dir.is_dir():
        click.echo(f"{dir} is not a directory")
        raise SystemExit(1)

    for file in dir.iterdir():
        if file.is_dir() and ext:
            continue
        if file.is_file() and not _validate_extension(file, ext):
            continue
        _print_output(file, long)


@cli.command()
@click.option(
    "-e",
    "--ext",
    type=click.STRING,
    help="File extension to zap the files (e.g .py)",
)
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def zd(path: Path, ext: str | None) -> None:
    """Zap current directory files"""


@cli.command()
def version():
    """Version of zap"""
    click.secho("zap version 0.0.1", fg="green")


if __name__ == "__main__":
    cli()
