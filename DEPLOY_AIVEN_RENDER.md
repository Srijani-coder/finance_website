# Deploy: Aiven PostgreSQL + Render + Cloudflare

## 1. Aiven database
Create a PostgreSQL service in Aiven. Copy the **service URI** (host, port, username, password, database). Configure the Aiven IP allowlist to permit connections from Render (Render outbound addresses may vary by plan/region; follow Render documentation). Keep TLS enabled; `sslmode=require` is added automatically if missing. Use a dedicated DB user with least privilege after initial setup.

## 2. GitHub and Render
Put this repository on GitHub privately. Create a Render Python web service and select the repository. **If the repository contains the `finance_site` directory at its root**, the included `render.yaml` Blueprint can be used as written. If you upload the *contents* of `finance_site` as repository root, remove `rootDir: finance_site` from `render.yaml`.

Build: `pip install -r requirements.txt`
Start: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app`
Health check: `/healthz`

Set `DATABASE_URL` to your Aiven URI, `SECRET_KEY` to a long random string, `ADMIN_PASSWORD` to a strong unique password (not `pass`), `SITE_URL` to your HTTPS domain, and `ADMIN_USERNAME` as desired. Configure Cloudinary variables for persistent CMS image uploads. Do not store uploaded images on Render's ephemeral disk.

The app creates tables on startup (`db.create_all`) and includes a basic compatibility patch for the admin username column. **This is not a full migration framework**; back up the database before schema changes. Do not use production credentials in source control.

## 3. Verify
Open `/healthz` and ensure HTTP 200. Test `/admin/login` (private, unlinked), `/admin/forgot`, username and password changes in CMS, signup, logout, protected pages, blog and image upload. Existing SQLite content is NOT automatically copied to Aiven. You must separately migrate any previous data you want to preserve.

## 4. Cloudflare custom domain
Add your domain under Render -> Settings -> Custom Domains. Follow the exact DNS values shown in Render and create them in Cloudflare. Start with DNS-only for verification; use Cloudflare Full (strict) TLS once Render HTTPS is valid. Set `SITE_URL` to the final HTTPS address.

## 5. Security before launch
Change default local credentials; enable Render HTTPS, use a strong secret, verify database firewall and TLS, and test permissions. This project still needs a full security audit, including CSRF protection, login rate limiting, production-safe schema migrations and access logging, before handling sensitive financial client data. Do not collect financial account details in the signup form.
