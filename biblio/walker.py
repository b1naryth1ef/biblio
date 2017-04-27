from __future__ import print_function

try:
    from itertools import imap, ifilter
except:
    imap = map
    ifilter = filter

import ast


class Walker(ast.NodeVisitor):
    filt = None

    def __init__(self, parser):
        self.parser = parser

    def get_docstring(self, node):
        return self.parser.parse(ast.get_docstring(node))

    def generic_visit(self, node):
        if not hasattr(self, 'visit_{}'.format(node.__class__.__name__)):
            print('WARNING: unvisited class: {}'.format(node))
            print(node.__dict__)
        return super(Walker, self).generic_visit(node)

    def visit_Module(self, node):
        obj = {
            'type': 'module',
            'docstring': self.get_docstring(node),
            'classes': [],
            'functions': [],
            'variables': [],
            'imports': [],
        }

        for node in imap(self.visit, node.body):
            if node['type'] == 'function':
                obj['functions'].append(node)
            elif node['type'] == 'class':
                obj['classes'].append(node)
            elif node['type'] == 'assign':
                obj['variables'].append(node)
            elif node['type'] in ('import', 'import_from'):
                obj['imports'].append(node)
            elif node['type'] in ('expr', ):
                continue

        return obj

    def visit_ClassDef(self, node):
        obj = {
            'type': 'class',
            'name': node.name,
            'docstring': self.get_docstring(node),
            'bases': list(ifilter(lambda k: k.get('name') != 'object', [
                {'name': i.id} if isinstance(i, ast.Name) else self.visit(i) for i in node.bases
            ])),
            'attributes': [],
            'functions': [],
        }

        for node in imap(self.visit, node.body):
            if node['type'] == 'function':
                obj['functions'].append(node)
            elif node['type'] == 'assign':
                obj['attributes'].append(node)

        return obj

    def visit_FunctionDef(self, node):
        return {
            'type': 'function',
            'docstring': self.get_docstring(node),
            'decorators': [],
            'name': node.name,
            'args': self.visit(node.args)
        }

    def visit_Assign(self, node):
        return {
            'type': 'assign',
            'targets': list(imap(self.visit, node.targets)),
            'value': self.visit(node.value)
        }

    def visit_Import(self, node):
        return {
            'type': 'import',
            'names': list(imap(self.visit, node.names))
        }

    def visit_ImportFrom(self, node):
        return {
            'type': 'import_from',
            'module': node.module,
            'names': list(imap(self.visit, node.names))
        }

    def visit_Name(self, node):
        return node.id

    def visit_Attribute(self, node):
        return {
            'type': 'attribute',
            'name': node.attr,
            'value': self.visit(node.value)
        }

    def visit_Load(self, node):
        return {
            'type': 'load',
        }

    def visit_Call(self, node):
        return {
            'type': 'call',
            'name': self.visit(node.func),
            # TODO: py3
            # 'starargs': node.starargs,
            # 'kwargs': node.kwargs,
            'keywords': list(imap(self.visit, node.keywords)),
            'args': list(imap(self.visit, node.args)),
        }

    def visit_Str(self, node):
        return node.s

    def visit_Num(self, node):
        return node.n

    def visit_Dict(self, node):
        return {
            'type': 'dict',
            'keys': list(imap(self.visit, node.keys)),
            'values': list(imap(self.visit, node.values)),
        }

    def visit_Set(self, node):
        return {
            'type': 'set',
            'elts': list(imap(self.visit, node.elts)),
        }

    def visit_List(self, node):
        return {
            'type': 'list',
            'elts': list(imap(self.visit, node.elts)),
        }

    def visit_Tuple(self, node):
        return {
            'type': 'tuple',
            'elts': list(imap(self.visit, node.elts)),
        }

    def visit_Lambda(self, node):
        return {
            'type': 'lambda',
            'args': self.visit(node.args),
        }

    def visit_NameConstant(self, node):
        return node.value

    def visit_keyword(self, node):
        return {
            'type': 'keyword',
            'arg': node.arg,
            'value': self.visit(node.value),
        }

    def visit_alias(self, node):
        return node.asname or node.name

    def visit_arguments(self, node):
        return {
            'args': list(imap(self.visit, node.args)),
            'defaults': list(imap(self.visit, node.defaults)),
            'kwargs': node.kwarg,
            'vargs': node.vararg,
        }

    def visit_arg(self, node):
        return node.arg

    def visit_Param(self, node):
        return {
            'type': 'param',
        }

    def visit_If(self, node):
        return {
            'type': 'if',
        }

    def visit_TryExcept(self, node):
        return {
            'type': 'try_except',
        }

    def visit_Expr(self, node):
        return {
            'type': 'expr',
        }

    def visit_Pass(self, node):
        return {
            'type': 'pass',
        }

    def visit_Add(self, node):
        return {
            'type': 'add',
        }

    def visit_BinOp(self, node):
        return {
            'type': 'bin_op',
        }

    def visit_Store(self, node):
        return {
            'type': 'store',
        }

    def visit_Subscript(self, node):
        return {
            'type': 'subscript',
        }

    def visit_Index(self, node):
        return {
            'type': 'index',
        }

    def visit_ExceptHandler(self, node):
        return {
            'type': 'except_handler',
        }

    def visit_Try(self, node):
        return {
            'type': 'try',
        }
