from tests import MoreFoundIn
from testutils import EXPECTED_MORE_FOUND, add_more_found_if_needed, eco, get_index_from_help, get_index_from_man, more_found
from pytest import mark
from tests.cargo import CARGO_TESTS
from tests.rsync import RSYNC_TESTS
from tests.tar import TAR_TESTS
from tests.uv import UV_TESTS


@mark.parametrize("command, expected, more_found_in", CARGO_TESTS + RSYNC_TESTS + TAR_TESTS + UV_TESTS)
class TestEco:
    # First compare with ++no-index
    # original default, expecteds are written without line indexes
    def test_without_index(self, command: str, expected: str, more_found_in: MoreFoundIn):
        expected = add_more_found_if_needed(command, expected, no_index=True, more_found_in=more_found_in)
        
        assert eco("++no-index " + command) == expected

    def test_with_index(self, command: str, expected: str, more_found_in: MoreFoundIn):
        # New default, as this is more informational with little clutter
        returned_lines: list[str] = eco(command).split("\n")
        
        expected = add_more_found_if_needed(command, expected, no_index=False, more_found_in=more_found_in)

        # Transform expected lines to add line index
        expected_lines: list[str] = expected.split("\n")
        for i in range(0, len(expected_lines)):
            line = expected_lines[i]
            if line.startswith("More results were"):  # TODO dynamic
                break
            if line.startswith("Results "):
                continue
            
            line_index = get_index_from_help(command, line) or get_index_from_man(command, line)
            expected_lines[i] = f"[{line_index}] {line}"
        
        # expected_lines += add_more_found_if_needed(command, expected, more_found_in).split("\n")
        # raise ValueError(expected_lines)
        # raise ValueError(expected_lines,returned_lines)

        # Compare lines
        for i in range(0, len(returned_lines)):
            returned_line = returned_lines[i]
            try: 
                expected_line = expected_lines[i]
            except IndexError:  # This will fail the result, but continue the test
                expected_line = ""
            
            if expected_line == "[0] " and returned_line == "":
                continue

            # Ensure first character is the index bracket
            #assert returned_line[0] == "["
            #assert expected_line[0] == "["

            assert returned_line == expected_line


# Handle '' in tests: it fucks up the run() call too
