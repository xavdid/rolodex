from cyclopts import App

from rolodex.sites.tildes import TildesConfig

app = App()
build = app.command(
    App(name="build", help="Build CSS for specific sites using these subcommands.")
)


build.command(**TildesConfig.to_cli())


if __name__ == "__main__":
    app()
