# Outlook email and password reset configuration

The admin password-reset email uses SMTP over STARTTLS on port 587. The supplied code supports SMTP username/password authentication, not OAuth2.

## Personal Outlook.com / Hotmail
1. Enable two-step verification on the Microsoft account.
2. If Microsoft offers an app-password option for your account, generate one. App passwords are not available for every account or authentication configuration.
3. Copy `.env.example` to `.env`, then set `SMTP_USER`, `SMTP_FROM` to the actual mailbox and `SMTP_PASSWORD` to the generated app password. Keep the file private.
4. Use `SMTP_HOST=smtp-mail.outlook.com` and `SMTP_PORT=587`.
5. Confirm SMTP AUTH is permitted for your account. Microsoft may reject password-based SMTP even with an app password; in that case an OAuth2-based email sender or transactional email provider is needed.

## Microsoft 365 work/school account
The typical server is `smtp.office365.com` on port 587 with STARTTLS. Modern tenants often disable basic SMTP authentication and require OAuth2. This project does **not** implement Microsoft OAuth2. Do not put your normal account password in `.env` expecting it to work. Use an OAuth2 implementation or a transactional email provider.

## Deployment
Set the same SMTP variables as private environment variables in Render. Never commit real credentials. Test the password-reset email before publishing. For production use a verified `SITE_URL` and strong `SECRET_KEY`. Admin reset emails should not be interpreted as proof that SMTP is working until delivery is confirmed.
