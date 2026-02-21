# Railway Root Directory Fix - Checklist

## ✅ Quick Fix (2-3 minutes)

### Problem
Root Directory fields have trailing spaces: `intellistack/content   `

### Solution
Remove spaces by retyping the paths

---

## 📋 Step-by-Step Checklist

### 1. Open Railway Dashboard
- [ ] Go to: https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c

### 2. Fix Backend Service
- [ ] Click on **backend** service
- [ ] Click **Settings** tab
- [ ] Find **Root Directory** field
- [ ] Select all text (Ctrl+A / Cmd+A)
- [ ] Delete it
- [ ] Type: `intellistack/backend` (no spaces!)
- [ ] Press Tab to save
- [ ] Click **Redeploy** button
- [ ] Wait for "Deploying..." status

### 3. Fix Auth-Server Service
- [ ] Go back to project view
- [ ] Click on **auth-server** service
- [ ] Click **Settings** tab
- [ ] Find **Root Directory** field
- [ ] Select all text (Ctrl+A / Cmd+A)
- [ ] Delete it
- [ ] Type: `intellistack/auth-server` (no spaces!)
- [ ] Press Tab to save
- [ ] Click **Redeploy** button
- [ ] Wait for "Deploying..." status

### 4. Fix Content Service
- [ ] Go back to project view
- [ ] Click on **content** service
- [ ] Click **Settings** tab
- [ ] Find **Root Directory** field
- [ ] Select all text (Ctrl+A / Cmd+A)
- [ ] Delete it
- [ ] Type: `intellistack/content` (no spaces!)
- [ ] Press Tab to save
- [ ] Click **Redeploy** button
- [ ] Wait for "Deploying..." status

### 5. Monitor Deployments
- [ ] Stay on Railway dashboard
- [ ] Watch each service deploy (5-10 minutes)
- [ ] Look for green checkmarks ✅
- [ ] If any fail, click to see error logs

---

## ✅ Success Indicators

After 5-10 minutes, you should see:
- ✅ Backend: Green checkmark, public URL assigned
- ✅ Auth-Server: Green checkmark, public URL assigned
- ✅ Content: Green checkmark, public URL assigned

---

## 🆘 If Still Failing

If services still fail after fixing:
1. Click on the failed service
2. Go to Deployments tab
3. Click on the failed deployment
4. Copy the error message
5. Share it with me for help
