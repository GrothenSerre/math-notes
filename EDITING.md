# Editing the website

The website is built with Quarto. Commits to `main` rebuild and publish it
automatically through GitHub Actions. You can make everyday edits directly
on GitHub without installing anything.

## Publish a blog post

1. Copy the contents of `templates/blog-post.qmd`.
2. On GitHub, open `blog/posts` and choose **Add file → Create new file**.
3. Name the file `your-title.qmd`, paste the template and write your text.
4. Set the title, date, description and categories. Remove `draft: true`.
5. Commit to `main`. The post appears in the blog and its RSS feed.

For a post with images, use `blog/posts/your-title/index.qmd` and upload its
images to that same folder. Link them with `![Description](image.jpg)`.

## Publish an essay or mathematics note

Use the same steps with the appropriate template and folder:

| Content | Template | Folder |
| --- | --- | --- |
| Blog post | `templates/blog-post.qmd` | `blog/posts/` |
| Essay | `templates/essay.qmd` | `essays/posts/` |
| Mathematics note | `templates/mathematics.qmd` | `mathematics/notes/` |

Lists update automatically. Keep `draft: true` while working on a piece;
remove it to publish. Use `$x^2$` for inline mathematics and `$$ ... $$`
for displayed equations. The mathematics template includes a theorem and proof.

## Upload a PDF or another downloadable file

- Upload mathematics files to `mathematics/files/`.
- Upload other files to `documents/files/`.

On GitHub, open the folder, choose **Add file → Upload files**, then commit.
New files are indexed automatically on the next build. Mathematics uploads
appear in both Mathematics and Documents; other uploads appear in Documents.
Use descriptive names such as `notes-on-derived-categories.pdf`.

To override a title or add a description, year or categories, add an entry to
`_data/documents.json`. The key is the file's path from the repository root:

```json
"documents/files/my-essay.pdf": {
  "title": "My Essay",
  "description": "A short description.",
  "categories": ["Philosophy"],
  "kind": "Essay",
  "year": "2026"
}
```

Remember to separate JSON entries with commas. Existing files stay at their
original paths so links to the original repository remain usable.

## Change the design or homepage

- Homepage: `index.qmd`
- Navigation, title and site URL: `_quarto.yml`
- Colours, typography and spacing: `assets/theme.scss`

## Preview on your own computer (optional)

Install [Quarto](https://quarto.org/docs/get-started/), then run:

```sh
quarto preview
```

To build and check the website:

```sh
quarto render
python3 scripts/check_site.py
```

No R, LaTeX distribution or Python packages are needed for these pages.
Python 3 is needed for the small archive generator.

## GitHub Pages setup (once)

1. In this repository, open **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**.
3. Commit these website files to `main`, or run **Actions → Build and publish
   Quarto website → Run workflow** if they were already committed.
4. Wait for the deployment to finish.

The intended address is **https://GrothenSerre.github.io/math-notes/**.
It is live only after the GitHub Pages deployment succeeds.
The workflow uses GitHub's built-in token; no personal access token is needed.
