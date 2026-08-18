import tomllib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self

from pydantic import BaseModel


class User(BaseModel):
    username: str
    color: str | None = None
    note: str | None = None


def css_comment(s) -> str:
    return f"/* {s} */"


class BaseSiteConfig(BaseModel, ABC):
    users: list[User]

    @property
    @abstractmethod
    def site_name(self) -> str: ...

    @classmethod
    def from_path(cls, path: Path) -> Self:
        return cls.model_validate(tomllib.loads(path.read_text()))

    def css_block(self, user: User) -> str:
        raise NotImplementedError

    def to_css(self) -> str:
        lines = [
            css_comment("THIS IS A GENERATED FILE"),
            css_comment("Any manual changes will be overwirtten"),
            "",
            css_comment(
                f"These styles were generated for {self.site_name} by `rolodex`"
            ),
            css_comment("https://github.com/xavdid/rolodex"),
            "",
        ]

        lines.extend(self.css_block(u) for u in self.users)

        return "\n".join(lines)
