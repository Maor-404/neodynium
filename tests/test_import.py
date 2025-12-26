"""Basic test file to verify pytest can run tests."""


def test_import():
    """Test that basic imports work."""
    assert True


def test_simple_assertion():
    """Simple test to verify pytest execution."""
    result = 1 + 1
    assert result == 2
