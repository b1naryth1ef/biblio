# biblio

biblio is an extremely fast and simple documentation generator for Python. At its core, biblio is just a wrapper that transalates Pythons native AST into a structure that can then be formatted and outputted.

## Architecture

Unlike Sphinx, biblio does not run any of your code, only parse it. This results in a much faster and more reliable documentation generation process. Using the AST also allows biblio to generate rich and in-depth output.

## TODO

biblio is fukin wip man

- Fix module pathing
- Parse docstrings
- Cleanup AST flatten
  - Some edge cases here we so far just brush over
- Better file pathing in config
  - Allow multiple path sources
  - Rules should allow for include/exclude
  - all of this needs to respect module pathing
- Proper config
- Proper outputs
  - Markdown
  - HTML (themable? gitbook like?)
- Allow for live outputing, inotify -> rebuild module
- multiprocessing
