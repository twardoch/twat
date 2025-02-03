"""Test suite for twat."""

def test_version():
    """Verify package exposes version."""
    import twat
    assert twat.__version__

def test_plugin():
    """Verify plugin functionality."""
    import twat
    plugin = twat.Plugin()
    plugin.set("test", "value")
    assert plugin.get("test") == "value"
 