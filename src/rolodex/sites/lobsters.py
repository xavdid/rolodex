from textwrap import dedent
from typing import ClassVar

from rolodex.sites._base import BaseSiteConfig, User


class LobstersConfig(BaseSiteConfig):
    username_color: str = "#ff4500"

    site_name: ClassVar[str] = "Lobsters"
    filename: ClassVar[str] = "lobsters"
    url: ClassVar[str] = "https://lobste.rs/"

    def user_block(self, user: User) -> str:
        author_user = f'.byline > a.user_is_author[href="/~{user.username}"]::before'

        return dedent(f"""\
            /* mark highlighted authors without using their color */
            {author_user} {{
                content: "⊙ ";
                color: var(--color-fg-author);
            }}

            .byline > a[href="/~{user.username}"],
            {author_user} {{
                color: {user.color or self.username_color};
        """)
