from pathlib import Path

import pytest


@pytest.fixture
def valid_activision_user_string() -> str:
    return "Joy#1648235"


@pytest.fixture
def invalid_activision_user_string() -> str:
    return "Joy#999999999989"


@pytest.fixture
def empty_activision_user_string() -> str:
    return ""


@pytest.fixture
def html_page() -> str:
    html_path = Path(__file__).parent.parent / "html" / "joy_test_html.html"
    with open(str(html_path), "r") as html_file:
        html = html_file.read()
    return html
