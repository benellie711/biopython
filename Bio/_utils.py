# Copyright 2010 by Eric Talevich. All rights reserved.
# Copyright 2012 by Wibowo Arindrarto. All rights reserved.
#
# This file is part of the Biopython distribution and governed by your
# choice of the "Biopython License Agreement" or the "BSD 3-Clause License".
# Please see the LICENSE file that should have been included as part of this
# package.
"""Common utility functions for various Bio submodules."""


import os


def read_forward(handle):
    """Read through whitespaces, return the first non-whitespace line."""
    while True:
        line = handle.readline()
        # if line is empty or line has characters and stripping does not remove
        # them, return the line
        if (not line) or (line and line.strip()):
            return line


def _read_header(handle, length):
    """Read the specified number of characters from the given handle.

    Raise a ValueError("Empty file.") if the length of data read is zero. The
    reason for having a separate function for the header is it enables raising
    an empty file error if the length of the data read is zero. This might
    not always be the case later in the file.
    """
    data = handle.read(length)
    if not data:
        raise ValueError("Empty file.")
    if len(data) < length:
        raise ValueError("Improper header, cannot read %d bytes from handle" % length)
    return data


def trim_str(string, max_len, concat_char):
    """Truncate the given string for display."""
    if len(string) > max_len:
        return string[: max_len - len(concat_char)] + concat_char
    return string


def getattr_str(obj, attr, fmt=None, fallback="?"):
    """Return string of the given object's attribute.

    Defaults to the given fallback value if attribute is not present.
    """
    if hasattr(obj, attr):
        if fmt is not None:
            return fmt % getattr(obj, attr)
        return str(getattr(obj, attr))
    return fallback


def find_test_dir(start_dir=None):
    """Find the absolute path of Biopython's Tests directory.

    Arguments:
    start_dir -- Initial directory to begin lookup (default to current dir)

    If the directory is not found up the filesystem's root directory, an
    exception will be raised.

    """
    if not start_dir:
        # no callbacks in function signatures!
        # defaults to the current directory
        # (using __file__ would give the installed Biopython)
        start_dir = "."

    target = os.path.abspath(start_dir)
    while True:
        if os.path.isdir(os.path.join(target, "Bio")) and os.path.isdir(
            os.path.join(target, "Tests")
        ):
            # Good, we're in the Biopython root now
            return os.path.abspath(os.path.join(target, "Tests"))
        # Recurse up the tree
        # TODO - Test this on Windows
        new, tmp = os.path.split(target)
        if target == new:
            # Reached root
            break
        target = new
    raise ValueError(
        "Not within Biopython source tree: %r" % os.path.abspath(start_dir)
    )


def run_doctest(target_dir=None, *args, **kwargs):
    """Run doctest for the importing module."""
    import doctest

    # default doctest options
    default_kwargs = {"optionflags": doctest.ELLIPSIS}
    kwargs.update(default_kwargs)

    cur_dir = os.path.abspath(os.curdir)

    print("Running doctests...")
    try:
        os.chdir(find_test_dir(target_dir))
        doctest.testmod(*args, **kwargs)
    finally:
        # and revert back to initial directory
        os.chdir(cur_dir)
    print("Done")


if __name__ == "__main__":
    run_doctest()
