from shared import eco

EXPECTED_a = "--archive, -a            archive mode is -rlptgoD (no -A,-X,-U,-N,-H)\n"
def test_a():
    assert eco("rsync -a") == EXPECTED_a

EXPECTED_rlptgoD = EXPECTED_a + \
"""--recursive, -r          recurse into directories
--links, -l              copy symlinks as symlinks
--perms, -p              preserve permissions
--times, -t              preserve modification times
--group, -g              preserve group
--owner, -o              preserve owner (super-user only)
-D                       same as --devices --specials
"""
def test_rlptgoD():
    assert eco("rsync -rlptgoD") == EXPECTED_rlptgoD
    
EXPECTED_chmod = "--chmod=CHMOD            affect file and/or directory permissions\n"
def test_chmod():
    assert eco("rsync --chmod") == EXPECTED_chmod
