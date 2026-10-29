# Finance CMS Website — Render + Aiven PostgreSQL

A deploy-ready Flask finance/marketing website styled from the supplied olive/cream palette and supplied Nibeedita Marketing & Distribution Service Pvt. Ltd. logo.

## Features
- Responsive olive/cream finance website
- Admin CMS: `/admin/login`
- Admin can change business/display name, tagline, hero copy, cover image, contact details, About copy and social URLs
- Blog/financial insights CMS with featured image, SEO title and meta description
- Gallery upload/delete CMS
- PostgreSQL through `DATABASE_URL` (Aiven compatible, including `sslmode=require`)
- Cloudinary-ready media uploads for persistent production media; local upload fallback for development
- Dynamic XML sitemap, robots.txt, canonical tags, Open Graph metadata, FinancialService JSON-LD
- Render Blueprint (`render.yaml`) and Gunicorn
- Mobile responsive

## Local run
1. `python -m venv venv`
2. Activate venv
3. `pip install -r requirements.txt`
4. Set environment variables from `.env.example` (or rely on SQLite locally)
5. `python app.py`
6. Visit `http://127.0.0.1:5000`

Default local admin only if environment variables are absent:
- email: `admin@example.com`
- password: `change-me-now`
Change these in production using Render environment variables before first launch.

## Aiven PostgreSQL
Create an Aiven PostgreSQL service. Put its connection URI into Render as `DATABASE_URL`, for example:
`postgresql://USER:PASSWORD@HOST:PORT/defaultdb?sslmode=require`
Do not commit credentials.

## Render
Push this folder to GitHub, create a Render Blueprint/Web Service, and use `render.yaml`. Set `DATABASE_URL`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `SITE_URL` and Cloudinary variables in Render.

## Persistent images
Render's local filesystem is ephemeral. For production, configure Cloudinary variables. The CMS automatically uploads images there when configured.

## Custom domain
In Render, open the web service → Settings → Custom Domains → add your domain. Add the DNS records Render shows at your DNS provider. Set `SITE_URL=https://yourdomain.com` after DNS/SSL is active.

## SEO launch checklist
- Replace placeholder company/about/service/contact text with verified business content.
- Set a real custom domain and `SITE_URL`.
- Add unique SEO titles/descriptions to posts.
- Submit `/sitemap.xml` to Google Search Console.
- Add GA4 only after consent/privacy requirements are handled.
- Add Privacy Policy, Terms, and the regulatory disclosures appropriate to the exact financial services offered.

## Important finance-content note
The starter text is generic because the supplied requirement checklist does not provide verified registration, regulator/licence, products, pricing, branches, address, phone, or policy details. Do not publish claims about regulated services, returns, approvals, or credentials until verified.
