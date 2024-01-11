import sys

from dataclasses import dataclass
from queue import Queue


def read_input(file_name: str) -> Queue:
    with open(file_name, "r") as f:
        lines = f.read().strip().splitlines()
    queue = Queue()
    for line in lines:
        queue.put(line.strip())
    return queue


@dataclass
class File:
    name: str
    size: int

    def __hash__(self):
        return hash(self.name)


class Directory:
    def __init__(self, name):
        self.name = name
        self.files = set()
        self.directories = {}
        self.size = 0

    def add_directory(self, directory: "Directory"):
        self.directories[directory.name] = directory

    def add_file(self, file: File):
        self.files.add(file)
        self.size += file.size

    def __hash__(self):
        return hash(self.name)


def build_filesystem(lines: Queue, cwd: Directory) -> int:
    """
    Build the file system recursively, totaling the
    directory sizes along the way.
    """
    while not lines.empty():
        line = lines.get()
        if line.startswith("$"):
            if line.endswith("ls"):
                continue
            elif "cd" in line:
                _, command, name = line.split()
                # exit current directory
                if name == "..":
                    return cwd.size
                # start at the root dir. ignore.
                elif name == "/":
                    continue
                # add child directory's size to current directory
                # after building the child directory
                else:
                    cwd.size += build_filesystem(lines, cwd.directories[name])
        # add contents: files or directories
        else:
            if line.startswith("dir"):
                _, name = line.split()
                directory = Directory(name)
                cwd.add_directory(directory)
            else:
                size, name = line.split()
                file = File(name, int(size))
                cwd.add_file(file)
    return cwd.size


def sum_directories_under_size_limit(cwd, limit=100000) -> int:
    """
    Recursively traverse the file system and sum directory
    sizes under the limit.
    """
    total = cwd.size if cwd.size < limit else 0
    for directory in cwd.directories.values():
        total += sum_directories_under_size_limit(directory, limit)
    return total


def find_smallest_directory_to_delete(
        space_needed: int,
        cwd: Directory,
) -> int:
    """
    Recursively traverse the file system to find the directory
    with the smallest size that matches or exceeds the space
    needed.
    """
    if cwd.size < space_needed:
        return sys.maxsize
    smallest = cwd.size
    for directory in cwd.directories.values():
        smallest = min(
            smallest,
            find_smallest_directory_to_delete(space_needed, directory),
        )
    return smallest


if __name__ == "__main__":
    terminal_log = read_input(sys.argv[1])
    root = Directory("/")
    build_filesystem(terminal_log, root)
    total_size = sum_directories_under_size_limit(root)
    print("Part 1:", total_size)

    total_disk_space = 70000000
    required_free_space = 30000000
    min_space_to_delete = root.size - (total_disk_space - required_free_space)
    dir_size = find_smallest_directory_to_delete(min_space_to_delete, root)
    print("Part 2:", dir_size)
