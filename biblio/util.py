import os


def walk_path(path):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.py'):
                yield os.path.join(root, file_name)
