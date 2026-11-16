# SPARC Lab website — instructions for Claude

This repo is the SPARC Lab website, a plain static HTML site (no build step).
It is served by GitHub Pages at https://sparclab.github.io/Sparclab-website/ and
https://engineering.purdue.edu/~shreyas/SparcLab/ redirects to it.
Pushing to `main` publishes the site within 1–3 minutes.

## Every time you make a change
1. Run `git pull` first (other people also edit this site).
2. Make the requested edit.
3. Check that every new image/PDF link points to a file that exists, with the
   exact same upper/lower case (GitHub Pages is case-sensitive; macOS is not).
4. Show the user a short summary of what changed and ask before pushing.
5. `git add -A && git commit -m "<short description>" && git push`
6. Tell the user the site will update in 1–3 minutes and give the page URL.

## Site conventions
- Pages are the `.html` files in the root. `index.html` is the home page.
- The nav menu is copied into every page. If a menu item changes, change it
  identically on all pages.
- Shared styling goes in `static/css/site.css`; shared JS in `static/js/site.js`.
  Don't add per-page `<style>` blocks for things that apply site-wide.
- Images go in `static/img/<section>/` (e.g. `static/img/news/`), media logos in
  `static/media_images/<year>/`, papers in `static/pdfs/j/` (journal),
  `static/pdfs/c/` (conference), `static/pdfs/p/` (patents).
- Use relative links (`static/img/...`, `news.html`), never
  `https://engineering.purdue.edu/~shreyas/SparcLab/...` and never `../`.
- Use simple file names for new uploads (no spaces; lowercase is safest).
- New items on News / Publications / Awards go at the top of their list,
  following the format of the existing entries.
- The Chip Gallery's light-blue background is intentional — keep it.
- Never delete pages or folders unless the user explicitly asks.
