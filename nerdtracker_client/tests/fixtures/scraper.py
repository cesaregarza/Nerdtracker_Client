import pytest


@pytest.fixture
def valid_activision_user_string():
    return "Joy#1648235"


@pytest.fixture
def invalid_activision_user_string():
    return "Joy#999999999989"


@pytest.fixture
def empty_activision_user_string():
    return ""
