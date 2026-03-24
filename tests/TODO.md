# Thorough Testing Plan

- [x] Add pytest to requirements.txt
- [x] Create tests/conftest.py: Fixtures for app, db, client
- [x] Create tests/test_app.py: Test health check, factory
- [x] Create tests/test_models.py: Test models, relationships, DB ops, edge cases (unique, enum, negative qty)
- [x] Install deps: pip install -r requirements.txt
- [x] Run pytest (multiple times, all pass)
- [x] Production DB: python -c "from app import init_db; init_db()"
- [ ] Test app manually (python app.py, curl /, browser)
- [ ] Integration tests after blueprints
