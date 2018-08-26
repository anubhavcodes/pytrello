import os
import pytest

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture()
def setup_tests_directory():
    return os.path.join(basedir, "tests")
