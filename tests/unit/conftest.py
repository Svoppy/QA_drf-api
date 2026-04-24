import pytest


@pytest.fixture(autouse=True)
def _enable_db_access_for_unit_tests(db):
    """Keep DB access explicit and stable for mutation runners."""
    return None
