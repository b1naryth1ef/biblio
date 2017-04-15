# biblio

biblio is an extremely fast and simple documentation generator for Python. At its core, biblio is just a wrapper that transalates Pythons native AST into a structure that can then be formatted and outputted.

## Architecture

Unlike Sphinx, biblio does not run any of your code, only parse it. This results in a much faster and more reliable documentation generation process. Using the AST also allows biblio to generate rich and in-depth output.

## TODO

biblio is fukin wip man

- Implement methdology for linking/parsing out types in data
  - We need to somehow extract types and modify the parsed docstrings to include links
- Proper HTML output
  - Theme
  - Search
- Allow for live outputting w/ inotify
- Multiprocessing
