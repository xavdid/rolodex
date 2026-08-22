from textwrap import dedent
from typing import ClassVar

from rolodex.sites._base import BaseSiteConfig, User


class TildesConfig(BaseSiteConfig):
    username_color: str = "#ff4500"

    site_name: ClassVar[str] = "Tildes"
    filename: ClassVar[str] = "tildes"
    url: ClassVar[str] = "https://tildes.net"

    def user_block(self, user: User) -> str:
        user_link = f'a.link-user[href$="/{user.username}"]'
        return dedent(f"""\
            .comment-header > {user_link},
            .topic-info-source > {user_link},
            .topic-full-byline > {user_link} {{
                color: {user.color or self.username_color};
        """)
