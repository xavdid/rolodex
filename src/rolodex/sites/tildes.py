from textwrap import dedent
from typing import ClassVar

from rolodex.sites._base import BaseSiteConfig, User


class TildesConfig(BaseSiteConfig):
    username_color: str = "#ff4500"

    site_name: ClassVar[str] = "Tildes"
    filename: ClassVar[str] = "tildes"
    url: ClassVar[str] = "https://tildes.net"

    def css_block(self, user: User) -> str:
        lines = dedent(f"""\
            .comment-header > a.link-user[href$="/{user.username}"],
            .topic-info-source > a.link-user[href$="/{user.username}"],
            .topic-full-byline > a.link-user[href$="/{user.username}"] {{
                color: {user.color or self.username_color};
        """)

        if user.note:
            lines += dedent(f"""
                /* needed to position the tooltip correctly */
                position: relative;

                &::after {{
                    content: "{user.note}";
                    /* positions to the right of the hover item */
                    position: absolute;
                    left: 100%;
                    /* centers the tooltip vertically */
                    top: 50%;
                    transform: translateY(-50%);
                    margin-left: 8px;

                    /* hover style */
                    background: #333;
                    color: #fff;
                    border: 1px solid #FFCB05;
                    padding: 4px 8px;
                    border-radius: 3px;
                    /* hidden until hovered */
                    visibility: hidden;
                }}

                &:hover::after {{
                    visibility: visible;
                }}
            }}
            """)
        else:
            lines += "}\n"

        return lines
