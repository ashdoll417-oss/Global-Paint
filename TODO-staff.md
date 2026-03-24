# Staff Site TODO

## Plan Implementation Steps

### 1. Requirements & Setup [x]
- [x] Update staff_site/requirements.txt (already complete)
- [ ] Ensure .env has STAFF_ACCESS_CODE

### 2. Core Files [x]
- [x] Rewrite staff_site/app/routes.py (access check, dashboard view query, sale form insert)
- [ ] Update staff_site/app/__init__.py (minor)

### 3. Templates [x]
- [x] Create staff_site/templates/base.html
- [x] Create staff_site/templates/access.html 
- [x] Create staff_site/templates/dashboard.html

### 4. Testing [ ]
- [ ] Run `cd staff_site && flask --app app run`
- [ ] Test access code → dashboard → record sale → verify DB insert
- [ ] Check staff_inventory_view displays correctly

### 5. Completion [ ]
- [ ] All checks pass
- [ ] Update this TODO with [x]

Current progress: Starting step 1.
