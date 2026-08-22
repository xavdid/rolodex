import pytest

from rolodex.sites._base import BaseSiteConfig


def test_class_vars_are_required():
    with pytest.raises(TypeError, match=r"must define") as e:

        class BadConfig(BaseSiteConfig):
            pass

    # there are 3 required properties, so there will be 2 commas
    assert str(e).count(",") == 2


def test_note_ends_with_brace():
    assert BaseSiteConfig.note_block("").strip().endswith("}\n}")
