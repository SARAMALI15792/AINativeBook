# Railway Setup Guide - Baby Steps

## Prerequisites
- A web browser (Chrome, Edge, Firefox)
- Your GitHub account (saramali15792)
- Your Neon PostgreSQL connection string (check your .env file)
- Your OpenAI API key (check your .env file)

---

## PART 1: Create Railway Account

### Step 1.1: Open Railway website
1. Open your browser
2. Type in the address bar: `https://railway.app`
3. Press Enter

### Step 1.2: Sign up with GitHub
1. You will see a landing page with a purple/dark theme
2. Look for a button that says **"Login"** in the top right corner
3. Click it
4. You will see options: "Login with GitHub", "Login with Email"
5. Click **"Login with GitHub"**
6. GitHub will ask you to authorize Railway
7. Click the green **"Authorize railway"** button
8. You are now logged into Railway!

---

## PART 2: Create a New Project

### Step 2.1: Start a new project
1. After logging in, you will see the Railway dashboard
2. Look for a button that says **"+ New Project"** (it's usually a purple button)
3. Click **"+ New Project"**

### Step 2.2: Choose empty project
1. A menu will appear with options like:
   - "Deploy from GitHub repo"
   - "Provision PostgreSQL"
   - "Empty Project"
2. Click **"Empty Project"**
3. You now have an empty project! It will look like a blank canvas with a grid background

### Step 2.3: Name your project
1. At the top of the page, you'll see a name like "project-abc-123"
2. Click on that name
3. Type: `intellistack`
4. Press Enter

---

## PART 3: Add the Backend Service

### Step 3.1: Add a new service
1. In your empty project, you'll see a **"+ New"** button (or "+ Add a Service")
2. Click it
3. A dropdown menu appears with options:
   - "GitHub Repo"
   - "Docker Image"
   - "Database"
   - "Empty Service"
4. Click **"Docker Image"**

### Step 3.2: Enter the Docker image name
1. A text box appears asking for the image name
2. Type exactly: `ghcr.io/saramali15792/intellistack-backend:latest`
3. Press Enter or click the confirm button
4. NOTE: This image won't exist yet until you push your code to GitHub. That's OK! We are setting it up first.

### Step 3.3: Rename the service
1. Click on the service box that appeared (it might say "ghcr-io-saramali15792...")
2. This opens the service detail panel
3. Click the **"Settings"** tab at the top
4. Find the field that says **"Service Name"**
5. Delete the current name
6. Type: `intellistack-backend`
7. Press Enter or click away to save

### Step 3.4: Generate a public URL for the backend
1. Still in the **"Settings"** tab
2. Scroll down to find the section called **"Networking"** or **"Public Networking"**
3. You will see a button that says **"Generate Domain"**
4. Click **"Generate Domain"**
5. Railway will create a URL like: `intellistack-backend-production-xxxx.up.railway.app`
6. **WRITE THIS URL DOWN** - you will need it later!
7. Copy it somewhere safe (a notepad, sticky note, etc.)

### Step 3.5: Add environment variables to the backend
1. Click the **"Variables"** tab at the top
2. You will see an empty area or a button that says **"+ Add Variable"** or **"RAW Editor"**
3. Click **"RAW Editor"** (this lets you paste multiple variables at once)
4. Paste the following (replace the placeholder values with your real values):

```
DATABASE_URL=postgresql://your-neon-username:your-neon-password@your-neon-host/your-database?sslmode=require
SECRET_KEY=replace-this-with-any-random-string-at-least-32-characters-long-abc123
ENVIRONMENT=production
CORS_ORIGINS=https://saramali15792.github.io
OPENAI_API_KEY=sk-your-openai-key-here
REDIS_URL=redis://localhost:6379/0
BETTER_AUTH_URL=http://localhost:3001
BETTER_AUTH_JWKS_URL=http://localhost:3001/.well-known/jwks.json
```

5. Click **"Update Variables"** or the save/confirm button

**Where to find your DATABASE_URL:**
- Open the file `intellistack/backend/.env` on your computer
- Look for the line that starts with `DATABASE_URL=`
- Copy that entire value

**Where to find your OPENAI_API_KEY:**
- Same `.env` file
- Look for `OPENAI_API_KEY=`
- Copy that value

**How to make a SECRET_KEY:**
- Just mash your keyboard to make a random string
- Example: `my-super-secret-key-a8f3k2j5m9p1q4w7`
- Must be at least 32 characters

---

## PART 4: Add the Auth Service

### Step 4.1: Go back to the project view
1. Click the **back arrow** or the project name at the top to go back to the project canvas view
2. You should see your backend service as a box

### Step 4.2: Add another new service
1. Click **"+ New"** again
2. Click **"Docker Image"**

### Step 4.3: Enter the auth Docker image name
1. In the text box, type exactly: `ghcr.io/saramali15792/intellistack-auth:latest`
2. Press Enter

### Step 4.4: Rename the auth service
1. Click on the new service box
2. Go to **"Settings"** tab
3. Change the **"Service Name"** to: `intellistack-auth`
4. Press Enter

### Step 4.5: Generate a public URL for the auth service
1. Still in **"Settings"** tab
2. Scroll to **"Networking"** or **"Public Networking"**
3. Click **"Generate Domain"**
4. Railway creates a URL like: `intellistack-auth-production-xxxx.up.railway.app`
5. **WRITE THIS URL DOWN TOO!**

### Step 4.6: Add environment variables to the auth service
1. Click the **"Variables"** tab
2. Click **"RAW Editor"**
3. Paste the following (replace placeholders with real values):

```
DATABASE_URL=postgresql://your-neon-username:your-neon-password@your-neon-host/your-database?sslmode=require
BETTER_AUTH_SECRET=replace-this-with-another-random-string-at-least-32-chars
BETTER_AUTH_URL=https://YOUR-AUTH-RAILWAY-URL-FROM-STEP-4.5
CORS_ORIGINS=https://saramali15792.github.io
PORT=3001
NODE_ENV=production
```

4. **IMPORTANT:** Replace `YOUR-AUTH-RAILWAY-URL-FROM-STEP-4.5` with the actual URL you wrote down in Step 4.5
   - Example: `https://intellistack-auth-production-xxxx.up.railway.app`
5. **IMPORTANT:** Use the SAME `DATABASE_URL` as the backend (same Neon database)
6. Click **"Update Variables"**

---

## PART 5: Cross-Link the Services

Now you need to tell the backend where the auth server lives.

### Step 5.1: Update backend variables
1. Go back to the project canvas (click back arrow or project name)
2. Click on the **`intellistack-backend`** service box
3. Go to the **"Variables"** tab
4. Find the variable `BETTER_AUTH_URL`
5. Click on its value to edit it
6. Change it from `http://localhost:3001` to: `https://YOUR-AUTH-RAILWAY-URL`
   - Example: `https://intellistack-auth-production-xxxx.up.railway.app`
7. Find the variable `BETTER_AUTH_JWKS_URL`
8. Change it to: `https://YOUR-AUTH-RAILWAY-URL/.well-known/jwks.json`
   - Example: `https://intellistack-auth-production-xxxx.up.railway.app/.well-known/jwks.json`
9. Click **"Update Variables"** or save

---

## PART 6: Generate a Deploy Token

This token lets GitHub Actions automatically deploy to Railway.

### Step 6.1: Go to account settings
1. Look at the **top right corner** of the Railway page
2. Click on your **profile picture** or **avatar**
3. A dropdown menu appears
4. Click **"Account Settings"**

### Step 6.2: Go to tokens
1. In the settings page, look at the left sidebar
2. Click **"Tokens"**

### Step 6.3: Create a new token
1. Click the **"+ Create"** or **"New Token"** button
2. Give it a name: `github-actions-deploy`
3. Click **"Create"**
4. A long string of text appears - this is your token
5. **COPY THIS TOKEN IMMEDIATELY** - you can only see it once!
6. Paste it somewhere safe temporarily (you'll add it to GitHub next)

---

## PART 7: Add Secrets to GitHub

### Step 7.1: Go to your GitHub repo settings
1. Open a new browser tab
2. Go to: `https://github.com/saramali15792/physicalhumoniodbook`
3. Click the **"Settings"** tab at the top of the page
   - (If you don't see Settings, make sure you're logged into GitHub as saramali15792)

### Step 7.2: Navigate to secrets
1. In the left sidebar, scroll down
2. Find **"Secrets and variables"**
3. Click the little arrow/triangle next to it to expand
4. Click **"Actions"**

### Step 7.3: Add the Railway token as a secret
1. Click the green **"New repository secret"** button
2. In the **"Name"** field, type exactly: `RAILWAY_TOKEN`
3. In the **"Secret"** field, paste the token you copied from Railway in Step 6.3
4. Click **"Add secret"**

### Step 7.4: Add repository variables
1. On the same page, look for a tab that says **"Variables"** (next to "Secrets" tab)
2. Click **"Variables"**
3. Click **"New repository variable"**

**Add these three variables one at a time:**

**Variable 1:**
- Name: `NEXT_PUBLIC_API_URL`
- Value: `https://YOUR-BACKEND-RAILWAY-URL` (the URL from Step 3.4)
- Click "Add variable"

**Variable 2:**
- Name: `NEXT_PUBLIC_AUTH_URL`
- Value: `https://YOUR-AUTH-RAILWAY-URL` (the URL from Step 4.5)
- Click "Add variable"

**Variable 3:**
- Name: `FRONTEND_URL`
- Value: `https://saramali15792.github.io`
- Click "Add variable"

---

## PART 8: Enable GitHub Pages

### Step 8.1: Navigate to Pages settings
1. Still in your repo **Settings** page
2. In the left sidebar, scroll down and click **"Pages"**

### Step 8.2: Set the source
1. Under **"Build and deployment"**
2. Find **"Source"**
3. There is a dropdown that probably says "Deploy from a branch"
4. Click the dropdown
5. Select **"GitHub Actions"**
6. That's it! No need to click save - it auto-saves

---

## PART 9: Push Your Code

### Step 9.1: Commit and push
1. Go back to your terminal/command prompt on your computer
2. Tell Claude Code: "commit and push all changes"

---

## PART 10: Verify Everything Works

### Step 10.1: Check GitHub Actions
1. Go to `https://github.com/saramali15792/physicalhumoniodbook`
2. Click the **"Actions"** tab
3. You should see workflows running (yellow spinning circle)
4. Wait for them to finish (green checkmark = success, red X = failed)

### Step 10.2: Check your sites
After the workflows finish:

1. **Frontend:** Open `https://saramali15792.github.io/`
   - You should see the IntelliStack landing page

2. **Docs:** Open `https://saramali15792.github.io/docs/`
   - You should see the Docusaurus content site

3. **Backend:** Open `https://YOUR-BACKEND-RAILWAY-URL/health`
   - You should see: `{"status": "healthy", ...}`

4. **Auth:** Open `https://YOUR-AUTH-RAILWAY-URL/health`
   - You should see: `{"status": "ok", ...}`

---

## TROUBLESHOOTING

### "Docker image not found" on Railway
This is normal if you haven't pushed your code yet. Railway will pull the image once GitHub Actions builds and pushes it.

### GitHub Actions workflow failed
1. Click on the failed workflow in the Actions tab
2. Click on the failed job
3. Read the red error messages
4. Common issues:
   - Missing secrets (check spelling of secret names)
   - npm install fails (dependency issues)

### Railway service won't start
1. Click on the service in Railway
2. Go to the **"Deployments"** tab
3. Click on the latest deployment
4. Read the logs for error messages
5. Common issues:
   - Wrong DATABASE_URL (check the connection string)
   - Missing environment variables

### Frontend loads but API calls fail
- Open browser DevTools (press F12)
- Go to Console tab
- Look for CORS errors
- Make sure the Railway URLs are correct in the GitHub variables

---

## SUMMARY: What URLs You Need to Save

| What | URL | Where You Get It |
|------|-----|-----------------|
| Frontend | `https://saramali15792.github.io/` | Automatic from GitHub Pages |
| Docs | `https://saramali15792.github.io/docs/` | Automatic from GitHub Pages |
| Backend API | `https://intellistack-backend-xxxx.up.railway.app` | Railway Step 3.4 |
| Auth Server | `https://intellistack-auth-xxxx.up.railway.app` | Railway Step 4.5 |
