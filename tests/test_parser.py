from unittest import TestCase


from biblio.parsers.numpy import NumPyParser, SECTIONS


COMPLEX_NUMPY_DOCSTRING = '''
This is a complex and detailed docstring for testing the numpy documentation syntax,
it spans multiple lines and includes multiple complex sections.

Attributes
----------
attr1 : int
    This is an attribute which has documentation spanning multiple lines, it's
    not a super exciting attribute, but it has its place.
attr2 : bool
    This attribute has some : colons in it : just to complicate things, and maybe
    even a few - dashes - here and there --:.
attr3 : dict(float, float)
    This one has a more complex function signature

Notes
-----
Here is a section with notes, it doesn't follow the rest of the sections because
it wnats to be different!

Returns
-------
bool
    A return section determines what this returns.

Yields
------
Optional[:class:`int`]
    Woaaaaaah a yield section, say whatt??
'''


class TestNumPyParser(TestCase):
    def test_finding_sections(self):
        parser = NumPyParser()
        sections = list(parser.get_sections(COMPLEX_NUMPY_DOCSTRING))
        self.assertEqual(len(sections), 5)

        for name, section in sections:
            self.assertTrue(name.lower() in SECTIONS + ['header'])

            for a, b, c in parser.get_section_content(section):
                self.assertTrue(c is not None)

    def test_parse(self):
        parser = NumPyParser()
        data = parser.parse(COMPLEX_NUMPY_DOCSTRING)

        self.assertEqual(data['raw'], COMPLEX_NUMPY_DOCSTRING)
        self.assertEqual(len(data['sections']), 5)
        self.assertEqual(len(data['sections']['header']), 1)
        self.assertEqual(len(data['sections']['yields']), 1)
        self.assertEqual(data['sections']['yields'][0]['content'], '\n    Woaaaaaah a yield section, say whatt??')
        self.assertEqual(len(data['sections']['attributes']), 3)
