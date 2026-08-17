from itertools import chain
from pathlib import Path

from rolodex.sites._base import BaseSiteConfig, User, css_comment, css_rule


class TildesConfig(BaseSiteConfig):
    username_color: str = "#ff4500"

    @property
    def site_name(self) -> str:
        return "Tildes"

    def css_block(self, user: User) -> list[str]:
        lines = [
            f'.comment-header > a.link-user[href$="/{user.username}"],',
            f'.topic-info-source > a.link-user[href$="/{user.username}"],',
            f'.topic-full-byline > a.link-user[href$="/{user.username}"] {{',
            f"  color: {user.color or self.username_color};",
        ]

        if user.note:
            lines.extend(
                [
                    "",
                    css_comment("needed to position the tooltip correctly", indent=2),
                    "",
                    css_rule("position", "relative", indent=2),
                    "",
                    "  &::after {",
                    css_rule("content", f'"{user.note}"', indent=4),
                    css_comment("positions to the right of the hover item", indent=4),
                    css_rule("position", "absolute", indent=4),
                    css_rule("left", "100%", indent=4),
                    css_comment("centers the tooltip vertically", indent=4),
                    css_rule("top", "50%", indent=4),
                    css_rule("transform", "translateY(-50%)", indent=4),
                    css_rule("margin-left", "8px", indent=4),
                    css_rule("position", "absolute", indent=4),
                    "",
                    css_comment("hover style", indent=4),
                    css_rule("background", "#333", indent=4),
                    css_rule("color", "#fff", indent=4),
                    css_rule("border", "1px solid #FFCB05", indent=4),
                    css_rule("padding", "4px 8px", indent=4),
                    css_rule("border-radius", "3px", indent=4),
                    css_comment("hidden until hovered", indent=4),
                    css_rule("visibility", "hidden", indent=4),
                    "  }",
                    "",
                    "  &:hover::after {",
                    css_rule("visibility", "visible", indent=4),
                    "  }",
                ]
            )

        lines.extend(["}", ""])

        return lines


# Path("tildes.css").write_text(
#     "\n".join(
#         [
#             *css_block("Deimos", "#ffb86c"),
#             *chain.from_iterable(
#                 css_block(u)
#                 for u in Path("users.txt").read_text().splitlines()
#                 if u and not u.startswith("#")
#             ),
#         ]
#     )
# )
