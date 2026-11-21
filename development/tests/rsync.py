from . import Scenario

RSYNC_TESTS: list[Scenario] = [
    Scenario(
        "rsync -a",
        "--archive, -a            archive mode is -rlptgoD (no -A,-X,-U,-N,-H)\n",
        "More found in manual"
    ),
    Scenario(
        "rsync -rlptgoD",
        """--archive, -a            archive mode is -rlptgoD (no -A,-X,-U,-N,-H)
--recursive, -r          recurse into directories
--links, -l              copy symlinks as symlinks
--perms, -p              preserve permissions
--times, -t              preserve modification times
--group, -g              preserve group
--owner, -o              preserve owner (super-user only)
-D                       same as --devices --specials
""",
        "More found in manual"
    ),

    Scenario(
        "rsync --chmod",
        "--chmod=CHMOD            affect file and/or directory permissions\n",
        "More found in manual"
    )
]
