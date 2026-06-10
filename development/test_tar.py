from testutils import eco

EXPECTED_xzvf = """  tar -xf archive.tar          # Extract all files from archive.tar.
  -x, --extract, --get       extract files from an archive
  -z, --gzip, --gunzip, --ungzip   filter the archive through gzip
  -v, --verbose              verbosely list files processed
  -f, --file=ARCHIVE         use archive file or device ARCHIVE
"""
def test_xzvf():
    assert eco("tar -xzvf") == EXPECTED_xzvf

EXPECTED_show_snapshot_field_ranges = """      --show-snapshot-field-ranges
                             show valid ranges for snapshot-file fields
"""
def test_show_snapshot_field_ranges():
    assert eco("tar --show-snapshot-field-ranges") == EXPECTED_show_snapshot_field_ranges