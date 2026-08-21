import tomllib
from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, ClassVar, Self, TypedDict

from cyclopts import Parameter, validators
from pydantic import BaseModel, ValidationError


class BuildConfig(TypedDict):
    obj: Callable[[Path, Path], int]
    name: str


class User(BaseModel):
    username: str
    color: str | None = None
    note: str | None = None


def css_comment(s) -> str:
    return f"/* {s} */"


class BaseSiteConfig(BaseModel, ABC):
    users: list[User]

    # config stuff; children should set these!
    site_name: ClassVar[str]
    """
    The common name of the site
    """
    filename: ClassVar[str]
    """
    the input and output toml files
    """
    url: ClassVar[str]
    """
    The URL of the website
    """

    def __init_subclass__(cls, **kwargs):
        """
        Runtime validation to ensure subclasses define expected variables. Runs when a class is declared.
        """
        super().__init_subclass__(**kwargs)
        if missing_vars := [
            attr
            for attr in ("site_name", "filename", "url")
            if attr not in cls.__dict__
        ]:
            raise TypeError(f"{cls.__name__} must define '{missing_vars}'")

    @classmethod
    def to_cli(cls) -> BuildConfig:
        """
        Returns the function that cyclopts wraps.
        """

        def fn(
            src: Annotated[
                Path,
                Parameter(
                    validator=validators.Path(exists=True, dir_okay=False, ext="toml"),
                    help="The source of the user data.",
                ),
            ] = Path(f"{cls.filename}.toml"),
            dest: Annotated[
                Path,
                Parameter(
                    validator=validators.Path(dir_okay=False, ext="css"),
                    help="The destination where the CSS file is written. Defaults to '\\<site\\>.css'",
                ),
            ] = Path(f"{cls.filename}.css"),
        ) -> int:  # returns the exit code for the CLI command
            try:
                config = cls.from_path(src)
                dest.write_text(config.to_css())
                print(f"Done! Wrote to {dest}")
                return 0
            except ValidationError as e:
                print(e)
                return 1

        fn.__doc__ = f"Generate CSS for {cls.site_name} ({cls.url})."

        return {"obj": fn, "name": cls.filename}

    @classmethod
    def from_path(cls, path: Path) -> Self:
        return cls.model_validate(tomllib.loads(path.read_text()))

    def to_css(self) -> str:
        """
        The top-level CSS file
        """

        return "\n".join(
            [
                css_comment("THIS IS A GENERATED FILE"),
                css_comment("Any manual changes will be overwirtten"),
                "",
                css_comment(
                    f"These styles were generated for {self.site_name} by `rolodex`"
                ),
                css_comment("https://github.com/xavdid/rolodex"),
                "",
                *(self.css_block(u) for u in self.users),
            ]
        )

    @abstractmethod
    def css_block(self, user: User) -> str: ...
