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

"""
cargo --help & cargo add --help are seperate help sections
Originally subcommand helps could only be searched using eco 'cargo add' (args)
...
"""
COMMAND_add_dev_with_quotes = "'cargo add' --dev"
EXPECTED_add_dev_with_quotes = """      --dev
          Add as development dependency
"""
def test_add_dev_with_quotes():
    assert eco(COMMAND_add_dev_with_quotes) == more_found(EXPECTED_add_dev_with_quotes, COMMAND_add_dev_with_quotes.replace("'", ""), man=True) 


"""
This was until f3f1338169fc03ae1e959a610fc0e877350968dd
Since that commit, cargo add (args) works and returns results
from main help & subcommand help
"""
COMMAND_add_dev_no_quotes = COMMAND_add_dev_with_quotes.replace("'", "")
EXPECTED_add_dev_no_quotes = """Results main command
    add         Add dependencies to a manifest file

Results subcommand
      --dev
          Add as development dependency
"""
def test_add_dev_without_quotes():
    assert eco(COMMAND_add_dev_no_quotes) == more_found(EXPECTED_add_dev_no_quotes, COMMAND_add_dev_no_quotes, man=True)

def test_add_dev_without_quotes_with_line_index():
    command = COMMAND_add_dev_no_quotes + " ++line"
    expected = EXPECTED_add_dev_no_quotes.split("\n")
    expected[1] = "29 " + expected[1]
    expected[4] = "125 " + expected[4]
    expected[5] = "126 " + expected[5]

    assert eco(command) == more_found("\n".join(expected), command, man=True)
