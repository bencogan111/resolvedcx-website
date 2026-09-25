# ResolvedCX website

Source for the new resolvedcx.com. Every change saved to the `main` branch rebuilds the site and republishes the preview in about a minute (see the **Actions** tab for progress). The preview address is under **Settings → Pages**. It's hidden from search engines.

## Where the text lives

| To change… | Edit this file |
|---|---|
| Anything on the home page (hero, Why ResolvedCX, comparison table, services, how it works, industries, Hubble quote, our story, FAQ, contact) | `src/template.html` |
| The service, industry and careers pages | `pages.py` (one block per page inside `PAGES = {...}`) |
| Privacy, Terms and Security pages | bottom of `src/template.html` (`<article class="legal" ...>`) |
| Menu, footer, contact-form address, Google Analytics | `build.py` (top of file and the `HEADER` / `FOOTER` sections) |
| Colors, fonts, spacing | `src/styles.css` |
| Photos, client logos, favicon, share image | `static/` |

## Making a quick edit on github.com

1. Open the file (for example `src/template.html`) and click the pencil icon.
2. Press Cmd+F (Ctrl+F on Windows) to find the sentence you want, then change the words between the tags. Leave the `<tags>` and `class="..."` alone.
3. Click **Commit changes**. The preview updates in a minute or two.

If something breaks, the **Actions** tab shows a red X. Open the file's **History** and revert the last change, or ask Claude to fix it.

## Editing with Claude

Claude Code (desktop app, or claude.ai/code) can open this repo directly. Ask in plain English, for example "Change the FAQ answer about pricing to say…" or "Add Jane Doe, Operations Manager, to the leaders list with this photo." It edits the files and commits them, and the preview rebuilds automatically.

## Building it yourself (optional)

Only standard Python 3 is needed:

```
python3 build.py             # full site in prod/, ready for www.resolvedcx.com
python3 build.py --preview   # single-file preview in preview/index.html
```

## Before going live on resolvedcx.com

1. **Hosting.** Point resolvedcx.com at this repo. You can add it as a custom domain in Settings → Pages, or connect the repo to Netlify or Cloudflare Pages (build command `python3 build.py`, output folder `prod`). For the live domain, build without `SITE_URL` so search engines can index it.
2. **Contact form.** Create a form at Formspree (or similar) that emails michael@resolvedcx.com, and paste its URL into `FORM_ENDPOINT` at the top of `build.py`. Until then, the form asks visitors to email Michael.
3. **Analytics.** Paste a Google Analytics 4 ID into `GA_ID` at the top of `build.py`.
4. **Placeholders.** Fill in the mailing address and applicant-retention period in the Privacy page, and have counsel review Privacy, Terms and Security (they're marked Draft).
5. **Old URLs.** Redirect /solutions → /services/customer-support/, /team → /#story, /contact-us → /#contact, /blog → /.
6. **Google Search Console.** Verify the domain and submit `https://www.resolvedcx.com/sitemap.xml`.
