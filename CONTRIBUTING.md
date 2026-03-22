# Contributing to LEETAPU

Thanks for contributing to this repository.

This project is a LeetCode solutions archive plus a website that is generated automatically from the solution files in the repository root. The website is deployed with GitHub Pages.

## Repository Structure

- Solution files live in the repository root.
- Website files live in `docs/`.
- Website data is generated automatically into `docs/assets/data/solutions.json`.
- Build scripts live in `scripts/`.
- GitHub Pages deployment is handled by `.github/workflows/deploy-pages.yml`.

## Solution File Naming

Please keep the filename format consistent:

```text
<number>. <Problem Title>.<extension>
```

Examples:

```text
1886. Determine Whether Matrix Can Be Obtained By Rotation.py
41. First Missing Positive.cpp
102. Binary Tree Level Order Traversal.java
```

Important:

- Put solution files in the repository root, not inside `docs/`.
- Keep the problem number at the beginning.
- Use a clear problem title.
- Use the correct language file extension.

## Supported Languages

The site currently recognizes these file extensions:

- `.py`
- `.cpp`
- `.cc`
- `.cxx`
- `.c`
- `.java`
- `.js`
- `.ts`
- `.cs`
- `.go`
- `.rb`
- `.php`
- `.swift`
- `.kt`
- `.rs`

## How the Website Updates

The website is generated from the files in the repository.

When a new solution file is added and pushed to `main`:

1. GitHub Actions runs the deploy workflow.
2. The site data is regenerated.
3. GitHub Pages is updated.
4. The new problem appears automatically in the website.

This also updates:

- today's latest problem
- latest uploads
- calendar archive
- search and filters
- in-site code viewer

## Local Development

To regenerate the website data locally:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\generate-site-data.ps1
```

To preview the site locally:

```powershell
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/docs/
```

## Contribution Guidelines

Please follow these rules when contributing:

- Do not change the solution filename format.
- Do not move solution files into folders unless the project structure is intentionally changed later.
- Avoid manually editing `docs/assets/data/solutions.json`.
  It is generated automatically.
- If you change the frontend or generator, make sure the local preview still works.
- Keep UI changes consistent with the current design direction.

## If You Add a New Solution

Recommended flow:

1. Add the new solution file in the repository root.
2. Run the generator locally if needed.
3. Preview the site locally if you changed website-related files.
4. Commit and push your changes.

Example:

```powershell
git add .
git commit -m "Add solution for problem 1886"
git push origin main
```

## If You Change the Website

If you edit files inside `docs/`, `scripts/`, or `.github/workflows/`:

- verify the generator still runs
- verify the site still opens locally
- make sure GitHub Pages deployment logic is not broken

Useful checks:

```powershell
node --check docs\app.js
powershell -ExecutionPolicy Bypass -File scripts\generate-site-data.ps1
```

## Pull Requests

If you open a pull request:

- describe what changed
- mention whether you added a solution, changed the UI, or updated deployment logic
- mention any local checks you ran

## Notes

The website uses git history to determine:

- first commit date
- file added dates
- today's latest problem
- archive entries by date

So preserving clean git history for new files helps the website stay accurate.
