# Nitin Bisht academic website

A static academic website with Home, Publications, Talks & Others, and CV pages. All website files, editable sources, and the current CV are in the repository root.

Repository: [kalpiree/kalpiree.github.io](https://github.com/kalpiree/kalpiree.github.io). Website address after publication: [https://kalpiree.github.io/](https://kalpiree.github.io/).

## Publish with GitHub Pages

1. Open the `kalpiree/kalpiree.github.io` repository and review its current contents.
2. Add all files from this folder directly to the repository root on the `main` branch. Keep the files at the top level, including `.nojekyll`; do not upload an enclosing folder or the ZIP file.
3. Open **Settings > Pages** in the repository.
4. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
5. Under **Branch**, choose **main** and **/(root)**, then click **Save**.
6. Wait for deployment, then use **Visit site** in **Settings > Pages**. GitHub documentation says publication can take up to 10 minutes.

The site uses root-relative links for the account website at `https://kalpiree.github.io/`. The empty `.nojekyll` file tells GitHub Pages to serve the prebuilt static files. No custom workflow is required.

Official GitHub instructions, checked 25 November 2026:

- [Creating a GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
- [Configuring a publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Edit and rebuild

Requires Python 3, with no third-party packages.

- `content.json`: research profile, publication titles, authors, links, and status.
- `build.py`: page structure, experience, teaching, talks, and professional development.
- `style.css` and `site.js`: layout and publication search.
- `nitin-bisht.jpg`, the two Noto Sans fonts, and their license: locally served visual assets.
- `nitin-bisht-cv.pdf`: replace the current CV using this filename.

Run from the repository root:

```bash
python3 build.py
python3 -m http.server 8000
```

Open `http://localhost:8000` to preview the website. Rebuilding writes only `index.html`, `publications.html`, `talks.html`, `cv.html`, and the empty `.nojekyll` marker. It does not delete or relocate files. After editing, commit both the source changes and regenerated HTML files to `main`. GitHub serves these prebuilt files; it does not run the Python build script.

Keep peer-reviewed publications separate from preprints and manuscripts. Preserve author order, equal-contribution markers, and confirmed status. The paper accepted at IJCAI 2025 is included in the preprint section.

## Assets

The layout is an original implementation inspired by compact academic sidebars and document-style sections. Nitin's portrait comes from his official ICDM 2026 workshop speaker profile. Noto Sans is bundled with its license in `NotoSans-LICENSE.txt`.
