from testutils import eco, get_index_from_help
from pytest import mark
from cargo import TESTS

@mark.parametrize("command, expected", TESTS)
class TestEco:
    # First compare with ++no-index
    # Original default, expecteds are written without line indexes
    def test_without_index(self, command: str, expected: str):
        assert eco("++no-index " + command) == expected

    def test_with_index(self, command: str, expected: str):
        # New default, as this is more informational with little clutter
        returned_lines: list[str] = eco(command).split("\n")

        # Transform expected lines to add line index
        expected_lines: list[str] = expected.split("\n")
        for i in range(0, len(expected_lines)):
            line = expected_lines[i]
            line_index = get_index_from_help(command, line)
            expected_lines[i] = f"[{line_index}] {line}"
        
        # Compare lines
        for i in range(0, len(returned_lines)):
            returned_line = returned_lines[i]
            expected_line = expected_lines[i]
            
            if expected_line == "[0] " and returned_line == "":
                continue

            # Ensure first character is the index bracket
            assert returned_line[0] == "["
            assert expected_line[0] == "["

            assert returned_line == expected_line



