import os
import fnmatch


def walk_path(path, rule):
    for root, dirs, files in os.walk(path):
        if '.git' in root:
            continue

        for file_name in files:
            path = os.path.join(root, file_name)[2:]
            if fnmatch.fnmatch(path, rule):
                yield path
