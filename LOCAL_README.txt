FINANCE WEBSITE - LOCAL DEMO
============================

This version runs completely on your computer. Render, Aiven PostgreSQL and Cloudinary are NOT required.
It uses a local SQLite database (site.db) and stores uploaded images under static/uploads/.

FIRST TIME ONLY
---------------
1. Install Python 3.10+.
2. Open Command Prompt in this finance_site folder.
3. Run:

   python -m pip install -r requirements-local.txt

START THE WEBSITE
-----------------
Run:

   python run.py

Or you can use:

   python app.py

Then open:
Website: http://127.0.0.1:5000
Admin:   http://127.0.0.1:5000/admin/login

DEFAULT LOCAL ADMIN
-------------------
Email:    admin@example.com
Password: change-me-now

LOCAL CMS DATA
--------------
- SQLite database: site.db (created automatically on first run)
- Uploaded cover/gallery/blog images: static/uploads/
- CMS changes remain available on the same computer after restart.

STOP SERVER
-----------
Press Ctrl+C in Command Prompt.
