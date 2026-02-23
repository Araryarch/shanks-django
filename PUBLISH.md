# Publishing Guide

Panduan untuk publish Shanks Django ke PyPI.

## Prerequisites

1. Install build tools:
```bash
pip install build twine
```

2. Buat akun di [PyPI](https://pypi.org/account/register/)

3. Buat API token di PyPI:
   - Login ke PyPI
   - Account Settings → API tokens
   - Create token dengan scope "Entire account"

## Build Package

1. Update version di `setup.py` dan `pyproject.toml`

2. Build distribution:
```bash
python -m build
```

Ini akan create files di folder `dist/`:
- `shanks-django-0.1.0.tar.gz` (source distribution)
- `shanks_django-0.1.0-py3-none-any.whl` (wheel)

## Test Upload (TestPyPI)

1. Upload ke TestPyPI dulu untuk testing:
```bash
twine upload --repository testpypi dist/*
```

2. Test install dari TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ shanks-django
```

## Production Upload (PyPI)

1. Upload ke PyPI:
```bash
twine upload dist/*
```

2. Masukkan username: `__token__`
3. Masukkan password: API token kamu (dimulai dengan `pypi-`)

## Verify

Test install:
```bash
pip install shanks-django
```

## Update Version

Untuk release baru:

1. Update version number di:
   - `setup.py`
   - `pyproject.toml`
   - `ace/__init__.py`

2. Commit changes:
```bash
git add .
git commit -m "Bump version to 0.2.0"
git tag v0.2.0
git push origin main --tags
```

3. Build dan upload ulang:
```bash
rm -rf dist/
python -m build
twine upload dist/*
```

## Automation (Optional)

Bisa pakai GitHub Actions untuk auto-publish saat create release.

Buat file `.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Tambahkan `PYPI_API_TOKEN` di GitHub repository secrets.

## Cara Setup GitHub Actions

1. Buat API token di PyPI:
   - Login ke https://pypi.org
   - Account Settings → API tokens
   - Create token dengan scope "Entire account" atau specific project

2. Tambahkan token ke GitHub:
   - Buka repository di GitHub
   - Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `PYPI_API_TOKEN`
   - Value: paste token dari PyPI

3. Cara publish dengan GitHub Actions:
   - Push code ke GitHub
   - Buat release baru di GitHub (Releases → Create a new release)
   - Tag version: `v0.1.0`
   - Publish release
   - GitHub Actions akan otomatis build dan upload ke PyPI

4. Manual trigger (optional):
   - Buka tab Actions di GitHub
   - Pilih workflow "Publish to PyPI"
   - Click "Run workflow"
