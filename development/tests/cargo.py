from . import Scenario

    

CARGO_TESTS = [
    Scenario("cargo -v", "  -v, --verbose...               Use verbose output (-vv very verbose/build.rs output)\n"),

    # Requires man fallback & no results for either mode fallback
    Scenario("cargo pkgid", """     cargo-pkgid(1)
         Print a fully qualified package specification.
"""),
    # Test searching in man cargo pkgid too

    
    # cargo --help & cargo add --help are seperate help sections
    # Originally subcommand helps could only be searched using eco 'cargo add' (args)
    # ...
    Scenario("'cargo add' --dev", """      --dev
          Add as development dependency
""", more_found_in="More found in manual"),

    # ...
    # This was until f3f1338169fc03ae1e959a610fc0e877350968dd
    # Since that commit, cargo add (args) works and returns results
    # from main help & subcommand help
    Scenario("cargo add --dev", """Results main command
    add         Add dependencies to a manifest file

Results subcommand
      --dev
          Add as development dependency
""", more_found_in="More found in manual")


]

 
