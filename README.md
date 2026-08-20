# rolodex

A small CLI to build and maintain custom CSS files that highlight specific users across certain sites.

![](https://cdn.zappy.app/7c8f651ac80401e8cc92e212b4c7ea5e.png)

Being able to recognize users is what turns a website into a community. It's a shame more sites don't support it natively.

Currently supports:

- [Tildes](https://tildes.net/)

Coming soon:

- Lobsters
- Hacker News

## Installation

You can install `rolodex` wherever you get your Python-based tools.

[uv](https://docs.astral.sh/uv/):

```shell
uv tool install rolodex
```

[mise](https://mise.jdx.dev/):

```shell
mise use -g pipx:rolodex
```

<!-- Using brew:

```shell
brew install xavdid/projects/rolodex
``` -->

## Usage

Applying custom styles to sites is simple enough, but it's a fairly manual process:

1. Write a users file
2. Generate css with `rolodex`
3. Paste those styles into [stylus](https://github.com/openstyles/stylus)
4. Refresh the page!

### 1. Write a users file

For each supported site, `rolodex` can parse a [toml](https://toml.io/en/) file with the following format:

```ts
{
  users: Array<{
    username: string;
    note?: string;
    color?: string; // supports any CSS value, like "#abcdef" or "pink"
  }>;
}
```

For example:

```toml
users = [
    { username = "some_username" },
    { username = "some_noted_username", note = "this is a note!" },
    { username = "some_colored_username", color = "#abcdef" },
]
```

### 2. Generate CSS

After you've [installed](#installation) `rolodex`, run it with the name of a supported site:

```shell
$ rolodex build tildes
# done! Wrote tildes.css
```

Uses `<sitename>.toml` (e.g. `tildes.toml`) as a default file, but you can pass any any filename.

### 3. Paste those styles into [stylus](https://github.com/openstyles/stylus)

You need a browser extension to apply your custom styles to supported sites. I use [stylus](https://github.com/openstyles/stylus) because it's popular and reputable, but there might be other options (Firefox [may support this](https://superuser.com/a/319322) natively?). Make sure to save.

### 4. Refresh the page!

Refresh any open pages for that site, and tada! Custom styles.

To add new users or notes, go back to [step 1](#1-write-a-users-file).
