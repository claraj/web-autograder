from shutil import copytree
import os

def combine(base, include, paths_to_overwrite, output_directory):
    """
    Combine two directories into a new directory given by output_directory
    The new directory will contain all the files from base, except for the paths specified by paths_to_overwrite
    List of paths given by paths_to_overwrite will contain files from these directories in include
    """

    print('OUT', output_directory)

    ignore_paths = [ os.path.join(base, p) for p in paths_to_overwrite ]
    splits = [ os.path.split(p) for p in ignore_paths ]  # heads and tails
    splits_dict = { p[0]:p[1] for p in splits }    # TODO cleanup

    # This function will be called with the current directory and a list of it's contents
    # Return a list of things to ignore
    def ignore_paths(directory, contents):
        for head, tail in splits_dict.items():
            if directory == head:
                return [tail]
        return []

    copytree(base, output_directory, ignore=ignore_paths)

    for path in paths_to_overwrite:
        source = os.path.join(include, path)
        destination = os.path.join(output_directory, path)
        print('copying', source, destination)
        copytree(source, destination)
