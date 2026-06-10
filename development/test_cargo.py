from testutils import eco

EXPECTED_v = "  -v, --verbose...               Use verbose output (-vv very verbose/build.rs output)\n"
def test_v():
    assert eco("cargo -v") == EXPECTED_v
