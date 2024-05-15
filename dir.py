import os


def print_dir_tree(start_path, skip_prefix='.'):
    """
    Prints the directory tree starting from 'start_path' skipping directories that start with 'skip_prefix'.

    Args:
    - start_path (str): The root directory from which to start the tree.
    - skip_prefix (str): Prefix to skip directories, default is '.' for hidden directories.
    """
    for root, dirs, files in os.walk(start_path, topdown=True):
        # Filter out directories to skip
        dirs[:] = [d for d in dirs if not d.startswith(skip_prefix)]

        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")

        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")





if __name__ == '__main__':
    print_dir_tree(os.getcwd())