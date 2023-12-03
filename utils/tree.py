import os
import fnmatch
from pathlib import Path


def read_gitignore(root_directory):
    gitignore_path = os.path.join(root_directory, '.gitignore')
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as gitignore_file:
            patterns = [line.strip() for line in gitignore_file if line.strip() and not line.startswith('#')]
            directory_patterns = [pattern for pattern in patterns if pattern.endswith('/')]
            file_patterns = [pattern for pattern in patterns if not pattern.endswith('/')]
            return directory_patterns, file_patterns
    return [], []


def should_ignore(path, directory_patterns, file_patterns, ignore_git_folder):
    if ignore_git_folder and path.split(os.sep)[0] == '.git':
        return True
    for pattern in directory_patterns:
        if path.endswith('/') and fnmatch.fnmatch(path, pattern):
            return True
    for pattern in file_patterns:
        if not path.endswith('/') and fnmatch.fnmatch(path, pattern):
            return True
    return False


def print_file_tree(current_directory,
                    root_directory,
                    directory_patterns, file_patterns,
                    output_style='indent',
                    indent_level=0,
                    write_to_file=False,
                    log_file_path=None,
                    ignore_git_folder=False):

    prefix = '    ' * indent_level if output_style == 'indent' else '|   ' * indent_level + '|-- ' if indent_level > 0 else ''

    for item in os.listdir(current_directory):
        path = os.path.join(current_directory, item)
        relative_path = os.path.relpath(path, root_directory) + ('/' if os.path.isdir(path) else '')

        if should_ignore(relative_path, directory_patterns, file_patterns, ignore_git_folder):
            continue

        masked_path = path.replace(root_directory, "~", 1) if output_style == 'indent' else path.replace(root_directory,
                                                                                                         '.', 1)
        output_line = f"{prefix}{masked_path}"

        if write_to_file:
            print(f"Logging {output_line} to {log_file_path}")
            with open(log_file_path, 'a') as log_file:
                log_file.write(output_line + '\n')
        else:
            print(output_line)

        if os.path.isdir(path):
            print_file_tree(path, root_directory, directory_patterns, file_patterns, output_style,
                            indent_level + 1, write_to_file, log_file_path, ignore_git_folder)


if __name__ == '__main__':

    project_root_directory = f"{Path(__file__).resolve().parent.parent}"
    dir_patterns, f_patterns = read_gitignore(project_root_directory)
    log_path = os.path.join(os.getcwd(), 'file_tree.log')

    logging_enabled = True
    style = 'tree',

    if logging_enabled:
        with open(log_path, 'w'):
            pass

    print_file_tree(
        project_root_directory,
        project_root_directory,
        dir_patterns, f_patterns,
        output_style=style,
        write_to_file=logging_enabled,
        log_file_path=log_path,
        ignore_git_folder=logging_enabled
    )
