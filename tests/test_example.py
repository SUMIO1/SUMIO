import pytest


def mult_by_2(x):
    if x is None:
        raise ValueError("x cannot be None")
    return x * 2

# if one of asserts fail, the remaining assets are not checked


def test_mult_by_2():
    assert mult_by_2(0) == 0
    assert mult_by_2(1) == 2
    assert mult_by_2(-1) == -2
    assert mult_by_2(10) == 20


def test_none():
    pytest.raises(ValueError, mult_by_2, None)


# even if one of (int_input, expected) tuple fails, the other tuples are still called
@pytest.mark.parametrize("int_input,expected", [
    (-2, -4),
    (-1, -2),
    (0, 0),
    (1, 2),
    (2, 4),
    (100, 200)
])
def test_multiple_values(int_input, expected):
    assert mult_by_2(int_input) is expected


# we can write a test but tell the pytest to skip it for now for some reason
# (for example we haven't implemented some feature yet)
@pytest.mark.skip(reason="reason for why pytest should skip this test")
def test_regex_slaps():
    assert True


# xfail - expected fail
# use to mark that you know that the test is not passed, but you still want the build to pass the test
# we basically ignore the facts that this test fails
@pytest.mark.xfail
def test_divide_by_zero():
    assert 1 / 0 == 1


# if you need to perform the same data preparing action in many different test, use fixtures

# and many, many more...
