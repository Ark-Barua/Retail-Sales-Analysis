# Live Deployment Architecture & Hosting Guide
**Project:** Enterprise Retail Sales Analysis & Predictive Performance Model  
**Author:** Ark Barua
---

## 1. Deployment Overview

This repository is designed with a **zero-dependency, modern client-side architecture**. The interactive dashboard (`dashboard/`) runs purely on HTML5, CSS3, and JavaScript with client-side dynamic CSV parsing. This means it can be hosted permanently for **free with zero ongoing maintenance or server overhead**.

| Hosting Platform | Deployment Effort | Cost | Custom Domain | Live URL Structure |
|---|---|---|---|---|
| **GitHub Pages (Recommended)** | Automated via GitHub Actions | **$0 / Free** | Supported | `https://<username>.github.io/<repo-name>/` |
| **Vercel** | 1-Click Git Import | **$0 / Free** | Supported | `https://<repo-name>.vercel.app/` |
| **Netlify** | 1-Click Drag or Git | **$0 / Free** | Supported | `https://<repo-name>.netlify.app/` |

---

## 2. Option A: GitHub Pages Deployment (Automated via GitHub Actions)

We have already configured `.github/workflows/deploy.yml` in this repository.

### Step-by-Step Instructions:
1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "feat: complete retail analytics and data science project"
   git push -u origin main
   ```
2. **Enable GitHub Pages in your repository settings:**
   - Go to your GitHub repository on `github.com`.
   - Click on **Settings** (gear icon in the top navigation).
   - In the left sidebar, click on **Pages** (under "Code and automation").
   - Under **Build and deployment > Source**, select:
     `GitHub Actions` (Recommended) or `Deploy from a branch` (Branch: `main`, Folder: `/dashboard`).
3. **View your Live Site:**
   - The GitHub Actions workflow will automatically run and publish the dashboard in ~45 seconds.
   - Your live link will be:  
     `https://<your-username>.github.io/<your-repo-name>/`

---

## 3. Option B: 1-Click Deployment on Vercel

The included [`vercel.json`](file:///c:/Users/ASUS/Desktop/Data%20Analytics%20Projects/vercel.json) automatically routes traffic directly to the `dashboard/` directory.

### Quick Deploy:
1. Visit [vercel.com](https://vercel.com) and log in with your GitHub account.
2. Click **"Add New Project"** > **"Import"** your retail repository.
3. Keep default settings (Vercel automatically detects `vercel.json`).
4. Click **Deploy**.
5. Your project will be immediately live on a custom `.vercel.app` URL with automatic SSL.

---

## 4. Option C: 1-Click Deployment on Netlify

The included [`netlify.toml`](file:///c:/Users/ASUS/Desktop/Data%20Analytics%20Projects/netlify.toml) points the publish folder to `dashboard/`.

### Quick Deploy:
1. Go to [netlify.com](https://netlify.com) and click **"Add new site" > "Import an existing project"**.
2. Select your GitHub repository.
3. Netlify will auto-detect `publish = "dashboard"`. Click **Deploy site**.

---

## 5. Live Dashboard Capabilities in Production

Once deployed, the live web dashboard allows any hiring manager, recruiter, or stakeholder to:
1. **Explore the Executive View:** View the exact IBCS-style dashboard matching executive Google reporting standards.
2. **Upload Custom CSVs:** Drag & drop any company or Kaggle sales CSV to recalculate metrics dynamically in real time without refreshing or server dependencies.
3. **Inspect Data Science & Machine Learning:** Open the dedicated ML Intelligence drawer to review 2023 sales forecasts, K-Means RFM clusters, and Welch's T-Test hypothesis results.
4. **Download Master Deliverables:** Download the sample CSV template and master Excel model directly from the top navigation bar.
