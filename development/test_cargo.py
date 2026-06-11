from testutils import eco, more_found

EXPECTED_v = "  -v, --verbose...               Use verbose output (-vv very verbose/build.rs output)\n"
def test_v():
    assert eco("cargo -v") == EXPECTED_v

# Requires man fallback & no results for either mode fallback
EXPECTED_pkgid = """     cargo-pkgid(1)
         Print a fully qualified package specification.
"""
def test_pkgid():
    # The ubuntu-latest CI runner has 2 extra spaces on the output here
    assert eco("cargo pkgid") == EXPECTED_pkgid or\
        eco("cargo pkgid") == EXPECTED_pkgid.replace("c", "  c", count=1).replace("P", "  P", count=1)

COMMAND_add_dev = "'cargo add' --dev"
EXPECTED_add_dev = """      --dev
          Add as development dependency
"""
def test_add_dev_with_quotes():
    # This is originally the only way to get cargo add help info
    assert eco(COMMAND_add_dev) == more_found(EXPECTED_add_dev, COMMAND_add_dev.replace("'", ""), man=True) 

EXPECTED_TWO = """Results main command
    add         Add dependencies to a manifest file

Results subcommand
      --dev
          Add as development dependency
"""
# This is the expected behaviour after patching
def test_add_dev_without_quotes():
    command = COMMAND_add_dev.replace("'", "")
    assert eco(command) == EXPECTED_TWO
