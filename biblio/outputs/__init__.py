from .json import JSONOutput
from .html import HTMLOutput
from .markdown import MarkdownOutput


OUTPUTS = {
    'json': JSONOutput,
    'html': HTMLOutput,
    'markdown': MarkdownOutput,
}
