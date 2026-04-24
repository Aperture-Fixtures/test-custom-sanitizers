# Python custom sanitizer model pack

This model pack adds a Python `barrierGuardModel` for `re.match(...)`.

It marks the checked string argument as sanitized on branches where the
`re.match(...)` call evaluates to `true`.

The model is scoped to XSS-relevant kinds used by `py/reflective-xss`:
- `html-injection`
- `js-injection`

## Files

- `qlpack.yml`
- `models/reflected-xss-barrier-guards.yml`

## Create a CodeQL Database

Create a new CodeQL database from the project source code:

```bash
codeql database create db-python --language=python
```

To overwrite an existing database, use the `--overwrite` flag:

```bash
codeql database create db-python --language=python --overwrite
```

## Analyze with CodeQL CLI

```bash
codeql database analyze db-python \
  codeql/python-queries:codeql-suites/python-code-scanning.qls \
  --additional-packs=.github/codeql/extensions \
  --model-packs=local/python-custom-sanitizers \
  --format=sarifv2.1.0 \
  --output=results-with-model.sarif \
  --rerun
```
