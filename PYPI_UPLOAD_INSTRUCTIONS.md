# PyPI Upload Instructions

## Version 0.2.6 Ready for Upload

### Pre-Upload Checklist ✅
- [x] Version bumped to 0.2.6
- [x] CHANGELOG.md updated
- [x] All files formatted with Black
- [x] Build successful
- [x] Twine check passed
- [x] All tests passing

### Files Ready
```
dist/
├── shanks_django-0.2.6-py3-none-any.whl
└── shanks_django-0.2.6.tar.gz
```

### Upload Command

```bash
python -m twine upload dist/*
```

When prompted:
- Username: `__token__`
- Password: Your PyPI API token (starts with `pypi-`)

### Alternative: Using .pypirc

Create `~/.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE
```

Then upload:
```bash
python -m twine upload dist/*
```

### Alternative: Using Environment Variable

```bash
# Windows PowerShell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YOUR-API-TOKEN-HERE"
python -m twine upload dist/*

# Linux/Mac
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-API-TOKEN-HERE
python -m twine upload dist/*
```

### Verify Upload

After upload, verify at:
- https://pypi.org/project/shanks-django/
- Check version shows 0.2.6
- Check changelog is updated

### Test Installation

```bash
pip install --upgrade shanks-django
python -c "import shanks; print(shanks.__version__)"
# Should output: 0.2.6
```

### What's New in 0.2.6

- **New Command**: `shanks generate django`
  - Converts Shanks project to standard Django structure
  - Auto-generates urls.py from Shanks routes
  - Creates deployment-ready structure
  - Includes production requirements.txt
  - Generates deployment README

### Previous Versions on PyPI
- 0.2.5 - JWT Auth & Critical Bug Fixes
- 0.2.3 - Cache & Swagger fixes
- 0.2.2 - Initial release

### Notes
- Package name: `shanks-django`
- Import name: `shanks`
- CLI commands: `shanks`, `sorm`
- License: MIT
- Python: >=3.8

### After Upload

1. Create GitHub release tag `v0.2.6`
2. Update documentation website
3. Announce on social media
4. Update README badges if needed

## Ready to Upload! 🚀
