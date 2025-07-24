import click
from pathlib import Path


@click.group()
def cli():
    """Zap is a tool to say goodbye to your files"""
    pass


@cli.command()
@click.option(
    "-e", "--ext", type=click.STRING, help="File extension to search for (e.g .py)"
)
@click.argument("dir", type=click.Path(exists=True, path_type=Path))
def list(dir: Path, ext: str | None) -> None:
    """List current directory files"""
    if not dir.is_dir():
        click.echo(f"{dir} is not a directory")
        raise SystemExit(1)

    for file in dir.iterdir():
        if file.is_file():
            if ext:
                if file.suffix.lower() == ext.lower():
                    click.secho(
                        f"{file.name:{len(file.name) + 5}}", nl=False, fg="green"
                    )


@cli.command()
def version():
    """Version of zap"""
    click.echo("zap version 0.0.1")


if __name__ == "__main__":
    cli()
