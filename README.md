# agnocast_doc

Document is published at https://tier4.github.io/agnocast_doc/

## Development

### pre-commit

This repository uses [pre-commit](https://pre-commit.com/) to run [markdownlint](https://github.com/igorshubovych/markdownlint-cli) on every commit. The same hook is executed in CI, so installing it locally lets you catch (and auto-fix) Markdown lint errors before pushing.

Install once after cloning:

```bash
pip install pre-commit
pre-commit install
```

From then on, `git commit` will run `markdownlint --fix` automatically against the staged Markdown files.
