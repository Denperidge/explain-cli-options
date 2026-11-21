from . import Scenario

TAR_TESTS: list[Scenario] = [
    Scenario(
        "tar -xzvf",
        """  tar -xf archive.tar          # Extract all files from archive.tar.
  -x, --extract, --get       extract files from an archive
  -z, --gzip, --gunzip, --ungzip   filter the archive through gzip
  -v, --verbose              verbosely list files processed
  -f, --file=ARCHIVE         use archive file or device ARCHIVE
""",
        "More found in manual"
    ),
    Scenario(
        "tar --show-snapshot-field-ranges",
        """      --show-snapshot-field-ranges
                             show valid ranges for snapshot-file fields\n"""
    )
]
