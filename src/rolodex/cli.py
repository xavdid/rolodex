from pathlib import Path
from typing import Annotated

from cyclopts import App, Parameter, validators
from pydantic import ValidationError

from rolodex.sites._base import BaseSiteConfig
from rolodex.sites.tildes import TildesConfig

app = App()
build = app.command(
    App(name="build", help="Build CSS for specific sites using these subcommands.")
)

IN_FILE_ANNOTATION = Annotated[
    Path,
    Parameter(
        validator=validators.Path(exists=True, dir_okay=False, ext="toml"),
        help="The source of the user data.",
    ),
]
OUT_FILE_ANNOTATION = Annotated[
    Path,
    Parameter(
        validator=validators.Path(dir_okay=False, ext="css"),
        help="The destination where the CSS file is written. Defaults to '\\<site\\>.css'",
    ),
]


def _build(class_: type[BaseSiteConfig], src: Path, dest: Path) -> int | None:
    """Helper for st

    non-zero return value"""
    try:
        config = class_.from_path(src)
    except ValidationError as e:
        print(e)
        return 1

    dest.write_text(config.to_css())
    print(f"Done! Wrote to {dest}")


@build.command
def tildes(
    src: IN_FILE_ANNOTATION = Path("tildes.toml"),
    dest: OUT_FILE_ANNOTATION = Path("tildes.css"),
):
    """
    Generate CSS for https://tildes.net.
    """
    return _build(TildesConfig, src, dest)


if __name__ == "__main__":
    app()
