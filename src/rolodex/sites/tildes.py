from textwrap import dedent
from typing import ClassVar

from rolodex.sites._base import BaseSiteConfig, User


class TildesConfig(BaseSiteConfig):
    username_color: str = "#ff4500"

    site_name: ClassVar[str] = "Tildes"
    filename: ClassVar[str] = "tildes"
    url: ClassVar[str] = "https://tildes.net"

    def user_block(self, user: User) -> str:
        return dedent(f"""\
            .comment-header > a.link-user[href$="/{user.username}"],
            .topic-info-source > a.link-user[href$="/{user.username}"],
            .topic-full-byline > a.link-user[href$="/{user.username}"] {{
                color: {user.color or self.username_color};
        """)
