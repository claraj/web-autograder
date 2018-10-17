from shutil import copytree, ignore_patterns
import os

def combine(base, include, paths_to_overwrite, output_directory):
    """ Combine two directories into a new directory given by output_directory
    The new directory will contain all the files from base,
    List of paths given by paths_to_overwrite will contain files from include
    """

    print(base)
    print(include)
    print(output_directory)

    ignore_from_base = ignore_patterns(*paths_to_overwrite)

    copytree(base, output_directory)

    for path in paths_to_overwrite:
        source = os.path.join(include, path)
        destination = os.path.join(base, path)
        copytree(source, destination)

    input('copy happened, go check, and then press ok to continue')
