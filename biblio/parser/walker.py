import ast

from biblio.parser.util import recursive_flatten_object

"""
This module needs to be refactored, ideally flatten takes a node and then recurses
vs the current structure of flatten taking a module and operating weirdly, there
is some duplicated code here. Ideally this is basically an ast walker, that we
could even eventually (or when we rewrite) just plug into the walker, and remove
the entire middle to_json step
"""


def ast_to_dict(source_code):
    node = ast.parse(source_code)
    node_info = recursive_flatten_object(node)
    node_info['_type'] = node.__class__.__name__
    return node_info


def flatten_generic(obj):
    if obj['_type'] == 'Num':
        return {
            'type': 'number',
            'value': obj['n'],
        }
    elif obj['_type'] == 'Name':
        return obj['id']
    elif obj['_type'] == 'Attribute':
        return {
            'type': 'attr',
            'parent': flatten_generic(obj['value']),
            'name': obj['attr'],
        }
    elif obj['_type'] == 'Call':
        return {
            'type': 'call',
            'func': flatten_generic(obj['func']),
            'keywords': [
                {'name': kw['arg'], 'value': flatten_generic(kw['value'])}
                for kw in obj['keywords']
            ],
        }
    elif obj['_type'] == 'Str':
        return {
            'type': 'str',
            'value': obj['s']
        }
    elif obj['_type'] in ('Set', 'List', 'Dict', 'Tuple', 'BinOp'):
        # TODO figure out what metadata to dump for these
        return {
            'type': obj['_type'].lower(),
        }

    print 'generic: {}'.format(obj['_type'])
    print obj


def flatten(module):
    assert(module['_type'] == 'Module')

    result = {
        'type': 'module',
        'docs': module['_docstring'],
        'imports': [],
        'classes': [],
        'functions': [],
        'variables': [],
    }

    for node in module['body']:
        if node['_type'] in ('Import', 'ImportFrom'):
            result['imports'] += list(flatten_imp(node))
        elif node['_type'] == 'Assign':
            result['variables'] += list(flatten_assign(node))
        elif node['_type'] == 'FunctionDef':
            result['functions'] += list(flatten_function(node))
        elif node['_type'] == 'ClassDef':
            result['classes'] += list(flatten_cls(node))
        else:
            print 'unparsed node {}'.format(node['_type'])

    return result


def flatten_assign(assign):
    # TODO: handle value
    for target in assign['targets']:
        yield {
            'name': flatten_name(target),
            'value': flatten_generic(assign['value']),
        }


def flatten_imp(imp):
    for name in imp['names']:
        obj = {
            'name': name,
            'module': None,
        }

        if imp['_type'] == 'ImportFrom':
            obj['module'] = imp['module']

        yield obj


def flatten_function(function):
    # TODO: turn args/kwarg/default/vararg into better signature

    yield {
        'name': function['name'],
        'docs': function['_docstring'],
        'args': map(flatten_name, function['args']['args']),
        # 'defaults': [i['n'] for i in function['args']['defaults']],
        'kwarg': function['args'].get('kwarg'),
        'vararg': function['args'].get('vararg'),
    }


def flatten_cls(cls):
    obj = {
        'name': cls['name'],
        'docs': cls['_docstring'],
        'bases': map(flatten_name, cls['bases']),
        'attributes': [],
        'functions': [],
    }

    for item in cls['body']:
        if item['_type'] == 'Assign':
            obj['attributes'] += list(flatten_assign(item))
        elif item['_type'] == 'FunctionDef':
            obj['functions'] += list(flatten_function(item))

    yield obj


def flatten_name(obj):
    if obj['_type'] == 'Name':
        return obj['id']
    elif obj['_type'] == 'Call':
        if obj['func']['_type'] == 'Attribute':
            return obj['func']['attr']
        else:
            return obj['func']['id']
    elif obj['_type'] == 'Attribute':
        return obj['attr'] + '.' + obj['value']['id']
    print 'unflattened name {}'.format(obj['_type'])
