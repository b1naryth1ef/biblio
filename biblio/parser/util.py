import os
import ast


def walk_path(path):
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if file_name.endswith('.py'):
                yield os.path.join(root, file_name)


def recursive_flatten_object(obj):
    result = {}

    for k, v in obj.__dict__.iteritems():
        if isinstance(v, ast.AST) or isinstance(v, dict):
            v = recursive_flatten_object(v)
        elif isinstance(v, list):
            v = map(recursive_flatten_object, v)
        result[k] = v

    if isinstance(obj, (ast.FunctionDef, ast.ClassDef, ast.Module)):
        result['_docstring'] = ast.get_docstring(obj)

    if isinstance(obj, ast.AST):
        result['_type'] = obj.__class__.__name__
    return result
