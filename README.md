# HTTP API Testing Example

Simple HTTP API testing example using python 3.9 and pytest

## installation
Execute in the terminal:
```bash
./install.sh
```

## Configuration

* SERVICE_URL - testing service URL, for e.g. http://localhost:3000
* USE_MOCK - boolean parameter for enabling/disabling request mocking

You can change it inside `framework/config.py` file or via environment variable:
```bash
export SERVICE_URL="http://localhost:3000"
export USE_MOCK="False"
```

## Testing

* With mocks (default parameter from `framework/config`):
```bash
pytest
```
* Without mocks:
```bash
USE_MOCK="False" pytest
```
* Another API URL:
```bash
SERVICE_URL="http://localhost:3000" USE_MOCK="False" pytest
```
