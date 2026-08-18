from rolodex.cli import app


def test_invalid_toml(tmp_path, capsys):
    src = tmp_path / "tildes.toml"
    src.write_text('users = [{color = "#abcdef"},{}]')

    result = app(
        ["build", "tildes", str(src)], result_action="return_int_as_exit_code_else_zero"
    )
    assert result == 1

    stdout = capsys.readouterr().out

    assert "users.0.username" in stdout
    assert "users.1.username" in stdout
    assert "type=missing" in stdout


def test_tildes_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    src = tmp_path / "tildes.toml"
    src.write_text('users = [{username = "example"}]')

    result = app(["build", "tildes"], result_action="return_int_as_exit_code_else_zero")
    assert result == 0

    dest = tmp_path / "tildes.css"
    assert dest.exists()

    output = dest.read_text()
    assert "/example" in output
    assert "#ff4500;" in output
    assert "&::after" not in output


def test_tildes_notes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    src = tmp_path / "tildes.toml"
    src.write_text('users = [{username = "example", note="wahoo"}]')

    result = app(["build", "tildes"], result_action="return_int_as_exit_code_else_zero")
    assert result == 0

    dest = tmp_path / "tildes.css"
    assert dest.exists()

    output = dest.read_text()
    assert "/example" in output
    assert "&::after" in output
    assert '"wahoo"' in output


def test_tildes_color(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    src = tmp_path / "tildes.toml"
    src.write_text('users = [{username = "example", color="#abcdef"}]')

    result = app(["build", "tildes"], result_action="return_int_as_exit_code_else_zero")
    assert result == 0

    dest = tmp_path / "tildes.css"
    assert dest.exists()

    output = dest.read_text()
    assert "/example" in output
    assert "&::after" not in output
    assert "#ff4500;" not in output
    assert "#abcdef;" in output


def test_tildes_with_path(tmp_path):
    src = tmp_path / "tildes.toml"
    dest = tmp_path / "tildes.css"
    src.write_text('users = [{username = "example"}]')
    assert (
        app(
            ["build", "tildes", "--src", str(src), "--dest", str(dest)],
            result_action="return_int_as_exit_code_else_zero",
        )
        == 0
    )
    assert dest.exists()
