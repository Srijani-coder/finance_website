# Olive & Cream Finance Portfolio — Local demo

1. Open a terminal in the `finance_site` folder.
2. Run `python -m pip install -r requirements-local.txt`.
3. Set `ADMIN_EMAIL`, `ADMIN_PASSWORD`, and `SECRET_KEY` in your environment before starting. For Windows PowerShell: `$env:ADMIN_EMAIL="you@example.com"`; `$env:ADMIN_PASSWORD="your-long-password"`; `$env:SECRET_KEY="random-long-secret"`.
4. Run `python run.py` and open `http://127.0.0.1:5000/`.
5. **Private admin route:** `/admin/login` (not linked anywhere on the public site). Bookmark it privately.

## CMS
Manage the owner's profile photo (a generic SVG placeholder is included), branding, contact details, Facebook/X/Instagram links, qualifications, chatbot answers, blog creation/edit/delete, and gallery photos. The gallery advances automatically every 5 seconds with previous/next and dots.

## Password recovery
Set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` for password-reset emails. The reset link expires after 30 minutes. For Gmail, use a Google app password where supported. Without working SMTP, the forgot-password form will not send email. Admin may change the password while logged in.

## Deployment/security notes
Hiding the admin link is **not** an access-control mechanism: login is required for all CMS functions. Change default demo credentials before making the site public. Use HTTPS, a strong `SECRET_KEY`, CSRF protection, rate limiting, trusted SMTP and a persistent storage service for production. Uploaded photos stored locally can disappear on ephemeral hosting; configure Cloudinary for persistent uploads. Existing SQLite installations receive additive settings columns on first startup. Blog content is displayed as plain text for safety. No certifications are claimed until the owner verifies them. The chatbot is a deterministic, editable FAQ assistant, not an AI model or regulated adviser.


Responsive layout updated for phone, tablet, laptop and desktop. Outlook SMTP configuration: see OUTLOOK_EMAIL_SETUP.md.


## October 2026 portfolio update
Home page is public; About, Services, Gallery, Blog, article and Contact routes require client registration/sign-in. Admin CMS at the private /admin/login route includes registration counts and client names/emails. Contact uses mailto: and does not need SMTP. Admin password changes are available while logged in; email password recovery is disabled. Partner names require verification and logos have intentionally not been fabricated. Existing database settings may override new defaults; update them in CMS. For production, set SECRET_KEY and strong ADMIN_PASSWORD, use PostgreSQL, HTTPS, and persistent image storage.
