---
document_type: PROMPT
status: ACTIVE
purpose: Create private GitHub repo "Experiment-JP" and push this workspace
---

# Git Setup — Private Repo "Experiment JP"

`gh` CLI was not available in the build environment. Follow these steps locally.

## 1. Create private repository on GitHub

1. Go to https://github.com/new  
2. Repository name: **Experiment-JP** (GitHub does not allow spaces)  
3. Description: `ENGEN Jet Park — management reporting experiment`  
4. Visibility: **Private**  
5. Do **not** initialize with README (this workspace already has content)  
6. Create repository  

## 2. Point remote and push

```powershell
cd "C:\Temp\Experiment JP"

# Keep template origin as backup (optional)
git remote rename origin template-origin

# Add your new private repo (replace YOUR_USER)
git remote add origin https://github.com/YOUR_USER/Experiment-JP.git

git push -u origin master
```

If your default branch is `main`:

```powershell
git branch -M main
git push -u origin main
```

## 3. Verify

- All `reports/`, `scripts/`, `docs/_ai_context/` should be on the remote  
- Confirm `.env` and secrets are **not** committed (see `.gitignore`)  

## 4. Install GitHub CLI (optional, for future PRs)

```powershell
winget install GitHub.cli
gh auth login
gh repo view
```
