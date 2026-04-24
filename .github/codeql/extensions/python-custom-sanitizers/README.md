# Python custom sanitizer model pack

This model pack adds a Python `barrierGuardModel` for the `validators.is_valid_file_id()` validator function.

It marks the checked string argument as sanitized on branches where the
`validators.is_valid_file_id()` call evaluates to `true`. This allows CodeQL to understand that
the validated `file_id` parameter is safe from XSS vulnerabilities when the validation function
returns true, preventing false positive alerts in code that guards against tainted input.

The model is scoped to XSS-relevant kinds used by `py/reflective-xss`:
- `html-injection`
- `js-injection`

## Files

- `qlpack.yml` — Pack metadata defining the extension target
- `models/reflected-xss-barrier-guards.yml` — Barrier guard model data for the validator function

## Implementation Notes: Module-Level Validator Functions

When implementing custom sanitizer models in CodeQL for Python, validator functions must be **defined in an imported module**, not inline within the main application code.

### The Problem: Local Function Definitions

Initially, `is_valid_file_id()` was defined locally in `app.py`. Even though the `barrierGuardModel` data was correctly configured, CodeQL would not match the guard:

```python
# This does NOT work with CodeQL models
def is_valid_file_id(file_id: str) -> bool:
    return bool(re.match("^[A-Za-z0-9]+$", file_id))
```

The barrier guard model would fail to apply because CodeQL's API graph resolution cannot reliably track locally-defined functions within the module scope where they are called.

### The Solution: Exported Module Functions

Move the validator function to a dedicated module and import it:

**validators.py:**
```python
import re

def is_valid_file_id(file_id: str) -> bool:
    """CodeQL Custom Sanitizer - validate file_id matches alphanumeric pattern."""
    return bool(re.match("^[A-Za-z0-9]+$", file_id))
```

**app.py:**
```python
import validators

# Now the guard works because CodeQL can resolve validators.is_valid_file_id
if validators.is_valid_file_id(file_id):
    # file_id is now recognized as sanitized
```

**Model (reflected-xss-barrier-guards.yml):**
```yaml
- ["validators", "Member[is_valid_file_id].Argument[0]", "true", "html-injection"]
```

The `["validators", "Member[is_valid_file_id]..."]` syntax tells CodeQL to look for the function as a member of the `validators` module, which allows the API graph to properly resolve and apply the barrier guard.

## GitHub Advanced Security

When this repository is configured with GitHub Advanced Security, the custom sanitizer model pack is automatically discovered and applied during code scanning. CodeQL will detect the `.github/codeql/extensions/` directory structure and load the model definitions without any additional configuration.

Simply commit this extension pack to the repository and enable Advanced Security in your GitHub repository settings. The validator function will be recognized during analysis.

## Testing Locally

### Create a CodeQL Database

Create a new CodeQL database from the project source code:

```bash
codeql database create db-python --language=python
```

To overwrite an existing database, use the `--overwrite` flag:

```bash
codeql database create db-python --language=python --overwrite
```

### Analyze with CodeQL CLI

```bash
codeql database analyze db-python \
  codeql/python-queries:codeql-suites/python-code-scanning.qls \
  --additional-packs=.github/codeql/extensions \
  --model-packs=local/python-custom-sanitizers \
  --format=sarifv2.1.0 \
  --output=results-with-model.sarif \
  --rerun
```
