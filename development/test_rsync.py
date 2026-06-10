from testutils import eco, more_found

EXPECTED_a = "--archive, -a            archive mode is -rlptgoD (no -A,-X,-U,-N,-H)\n"
def test_a():
    command = "rsync -a"
    assert eco(command) == more_found(EXPECTED_a, command, True)

EXPECTED_rlptgoD = """--archive, -a            archive mode is -rlptgoD (no -A,-X,-U,-N,-H)
--recursive, -r          recurse into directories
--links, -l              copy symlinks as symlinks
--perms, -p              preserve permissions
--times, -t              preserve modification times
--group, -g              preserve group
--owner, -o              preserve owner (super-user only)
-D                       same as --devices --specials
"""
def test_rlptgoD():
    command = "rsync -rlptgoD"
    assert eco(command) == more_found(EXPECTED_rlptgoD, command, True)
    
EXPECTED_chmod = "--chmod=CHMOD            affect file and/or directory permissions\n"
def test_chmod():
    command = "rsync --chmod"
    assert eco(command) == more_found(EXPECTED_chmod, command, True)
