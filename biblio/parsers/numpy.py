import re

try:
    from itertools import izip
except ImportError:
    izip = zip

from biblio.parsers.base import BaseParser


SECTION_HEADER_RE = re.compile(r'(\w+)\n[-]+')
SECTION_CONTENT_RE = re.compile(r'^(\S+)(?:$|[ ]+:[ ]+?(.+))$', re.M)

SECTIONS = [
    'args',
    'arguments',
    'attributes',
    'example',
    'examples',
    'kwargs',
    'methods',
    'notes',
    'note',
    'parameters',
    'params',
    'return',
    'returns',
    'raises',
    'references',
    'todo',
    'see also',
    'warning',
    'warnings',
    'warns',
    'yield',
    'yields',
]


def nwise(iterable, n):
    return izip(*[
        iterable[i::n] for i in range(n)
    ])


class NumPyParser(BaseParser):
    def parse(self, docstring):
        result = {
            'raw': docstring,
            'sections': {}
        }

        if not docstring:
            return result

        for name, section in self.get_sections(docstring):
            if section in result:
                raise Exception('More than one section for {} defined'.format(section))

            parts = []
            for a, b, c in self.get_section_content(section):
                parts.append({
                    'name': a,
                    'type': b,
                    'content': c,
                })

            result['sections'][name.lower()] = parts

        return result

    def get_sections(self, docstring):
        parts = [i.strip() for i in SECTION_HEADER_RE.split(docstring)]
        if not len(parts):
            raise StopIteration

        # If the first part isn't in the sections, we can safely assume its the pre-doc comment
        if parts[0].lower() not in SECTIONS:
            yield 'header', parts.pop(0)

        for header, section in nwise(parts, 2):
            yield header, section

    def get_section_content(self, section):
        parts = SECTION_CONTENT_RE.split(section)

        if parts[0]:
            yield None, None, parts[0]

        for item in nwise(parts[1:], 3):
            yield item
