import pytest

from xloop import xloop, DEFAULT_NOT_ITERATE


@pytest.mark.parametrize(
    "param1, param2, expected",
    [
        (1, None, [1]),
        ("abc", ["def", "ghi"], ["abc", "def", "ghi"]),
        ([1, None, "abc"], [2, 3, [4]], [1, "abc", 2, 3, [4]]),
        (None, {"a": 1}, ["a"]),
        ([b"123", "234", 345], None, [b"123", "234", 345]),
        (None, None, [])
    ],
)
def test_loop_no_dict(param1, param2, expected):
    result = list(xloop(param1, param2))
    assert result == expected


def test_none():
    assert list(xloop()) == []
    assert list(xloop(None)) == []
    assert list(xloop(None, None)) == []
    assert list(xloop([None, None])) == []


@pytest.mark.parametrize(
    "param1, param2, expected",
    [
        (1, {"abc": 123, "def": [4, 5, 6]}, [1, "abc", "def"]),
        ({1: 3}, {"abc": 123, None: "none", "def": 4}, [1, "abc", "def"]),
    ],
)
def test_loop_w_dict(param1, param2, expected):
    result = list(xloop(param1, param2))
    assert result == expected


@pytest.mark.parametrize(
    "param1, param2, expected",
    [
        (1, {"abc": 123, "def": [4, 5, 6]}, [1, ("abc", 123), ("def", [4, 5, 6])]),
        (
            {1: 3},
            {"abc": 123, None: "none", "def": 4},

            # Reason `(None, "none")` is returned, is because the
            # yielded value of `None` != `(None, "none")`.
            [(1, 3), ("abc", 123), (None, "none"), ("def", 4)]
         ),
    ],
)
def test_loop_w_yield_items_for_dicts(param1, param2, expected):
    result = list(xloop(param1, param2, yield_items_for_dicts=True))
    assert result == expected


def test_w_not_iterate():
    loop_args = [
        321,
        ['hello', 'today'],
        {'k': 'v'}
    ]

    results = list(xloop(*loop_args, not_iterate=[str, dict]))
    assert results == [321, 'hello', 'today', {'k': 'v'}]

