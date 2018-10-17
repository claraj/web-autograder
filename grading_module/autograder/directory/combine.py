from shutil import copytree
import os

def combine(base, include, paths_to_overwrite, output_directory):
    """ Combine two directories into a new directory given by output_directory
    The new directory will contain all the files from base,
    List of paths given by paths_to_overwrite will contain files from include
    """

    print('BASE', base)
    print('INCL', include)
    print('OUT', output_directory)

    patterns = *paths_to_overwrite,
    print(patterns)

    # one pattern hack
    # Should ignore copy /src/main but keep /src/test /src/somethingelse etc.
    pattern = 'src/main'
    full_path = os.path.join(base, pattern)

    print('fullpath', os.path.split(full_path))


    # This function will be called with the current directory and a list of it's contents
    # Return a list of things to ignore
    def ignore_paths(directory, contents):

        print('should', directory, 'be ignored?')

        head, tail = os.path.split(full_path)
        if directory == head:
            print('ignoring', head, tail)
            return [tail]
        return []


    copytree(base, output_directory, ignore=ignore_paths)

    input('copy of instructor code happened')

    # for path in paths_to_overwrite:
    #     source = os.path.join(include, path)
    #     destination = os.path.join(output_directory, path)
    #     print('copying', source, destination)
    #     copytree(source, destination)


    source = os.path.join(include, pattern)
    destination = os.path.join(output_directory, pattern)
    print('copying', source, destination)
    copytree(source, destination)



    input('copy happened, go check, and then press ok to continue')
