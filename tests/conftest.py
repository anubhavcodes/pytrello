import os
import pytest


@pytest.fixture()
def setup_tests_directory():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(BASE_DIR, "tests")
