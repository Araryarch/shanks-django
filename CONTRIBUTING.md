# Contributing to Shanks Django

Terima kasih sudah tertarik untuk berkontribusi!

## Development Setup

1. Clone repository:
```bash
git clone https://github.com/Ararya/shanks-django.git
cd shanks-django
```

2. Buat virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -e .
pip install django
```

## Testing

Jalankan example:
```bash
python example.py
```

## Pull Request Process

1. Fork repository
2. Buat branch baru (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Buat Pull Request

## Code Style

- Gunakan Python 3.8+ syntax
- Follow PEP 8
- Tambahkan docstrings untuk functions/classes
