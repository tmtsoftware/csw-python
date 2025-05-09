import pytest

from csw.Separator import Separator


def test_sep():
    assert(Separator.hyphenate("aaa") == "aaa")
    assert(Separator.hyphenate("aaa", "bbb") == "aaa-bbb")
    assert(Separator.hyphenate("aaa", "bbb", "ccc") == "aaa-bbb-ccc")
