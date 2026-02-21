# Railway Root Directory Fix - Simple Guide

## 🚨 Problem

All Railway services are failing with:
```
Root Directory `intellistack/content   ` does not exist
```

**Root Cause:** Trailing spaces in the Root Directory fields (set in Railway dashboard)

---

## 🎯 Goal
Fix the Root Directory fields by removing trailing spaces so services can deploy successfully.

## ⏱️ Time Required
2-3 minutes total

---

## 📝 Step-by-Step Instructions

### Step 1: Open Railway Dashboard
Click this link or copy-paste into your browser:
```
https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c
```

You should see 4 services: **backend**, **auth-server**, **content**, and **Redis**

---

### Step 2: Fix Backend Service

1. **Click** on the **backend** service card
2. **Click** the **Settings** tab (top navigation)
3. **Scroll down** to find the **"Root Directory"** field
4. **Select ALL text** in that field (Ctrl+A or Cmd+A)
5. **Delete it completely**
6. **Type exactly**: `intellistack/backend` (no copy-paste!)
7. **Press Tab** to save the field
8. **Click** the **"Redeploy"** button (usually at the top right)

✅ Backend is now fixed!

---

### Step 3: Fix Auth-Server Service

1. **Click** the back arrow or project name to return to project view
2. **Click** on the **auth-server** service card
3. **Click** the **Settings** tab
4. **Scroll down** to find the **"Root Directory"** field
5. **Select ALL text** in that field (Ctrl+A or Cmd+A)
6. **Delete it completely**
7. **Type exactly**: `intellistack/auth-server` (no copy-paste!)
8. **Press Tab** to save the field
9. **Click** the **"Redeploy"** button

✅ Auth-Server is now fixed!

---

### Step 4: Fix Content Service

1. **Click** the back arrow or project name to return to project view
2. **Click** on the **content** service card
3. **Click** the **Settings** tab
4. **Scroll down** to find the **"Root Directory"** field
5. **Select ALL text** in that field (Ctrl+A or Cmd+A)
6. **Delete it completely**
7. **Type exactly**: `intellistack/content` (no copy-paste!)
8. **Press Tab** to save the field
9. **Click** the **"Redeploy"** button

✅ Content is now fixed!

---

## 🎉 Done!

All three services are now redeploying with the correct directories (no trailing spaces).

### What Happens Next?

Railway will:
1. Build each service (5-10 minutes)
2. Run database migrations for backend
3. Assign public URLs to each service
4. Start serving traffic

### Monitor Progress

Stay on the Railway dashboard and watch the deployment logs:
- **Green checkmark** = Deployed successfully ✅
- **Yellow spinner** = Building/Deploying ⏳
- **Red X** = Failed (check logs) ❌

---

## ✅ Success Criteria

After fixing, you should see:
- ✅ No "Root Directory does not exist" errors
- ✅ Docker build process starts successfully
- ✅ All services get public URLs
- ✅ Health endpoints respond

---

## 🔍 Verify Deployments

Once all services show green checkmarks, test the health endpoints:

```bash
# Check backend
curl https://intellistack-platform-production-backend.up.railway.app/health

# Check auth-server
curl https://intellistack-platform-production-auth-server.up.railway.app/health

# Check content
curl https://intellistack-platform-production-content.up.railway.app/health
```

All should return `{"status": "healthy"}`

---

## 🆘 If Something Goes Wrong

### If services still fail after fixing:

1. **Check the Root Directory field again**
   - Make sure there are NO spaces at the end
   - The field should show exactly: `intellistack/backend` (no trailing spaces)

2. **Check build logs**
   - Click on the failed service
   - Go to Deployments tab
   - Click on the failed deployment
   - Look for error messages

3. **Verify environment variables**
   ```bash
   railway service backend variables
   ```
   Should show all required variables

4. **Share error logs with me**
   - Copy the error message from Railway logs
   - I'll help diagnose and fix

---

## 📊 Expected Result

After configuration (in 5-10 minutes):

✅ **Backend**: Running at `https://intellistack-platform-production-backend.up.railway.app`
✅ **Auth-Server**: Running at `https://intellistack-platform-production-auth-server.up.railway.app`
✅ **Content**: Running at `https://intellistack-platform-production-content.up.railway.app`
✅ **Redis**: Connected to backend automatically

---

## 🚀 Alternative: Use Helper Scripts

If you prefer automated guidance:

### Option 1: Interactive Python Script
```bash
python fix-railway-root-directory.py
```

### Option 2: Windows Batch Script
```bash
fix-railway-root-directory.bat
```

### Option 3: Follow Checklist
See `RAILWAY_FIX_CHECKLIST.md` for a detailed checklist

---

## 🎯 Next Steps After Successful Deployment

Once all services are deployed:

1. **Test health endpoints** (see Verification section above)
2. **Check database connectivity** (backend should connect to Neon)
3. **Verify Redis connection** (all services should connect)
4. **Test authentication flow** (auth-server OIDC endpoints)
5. **Monitor logs** for any runtime errors

---

**Go ahead and fix the services now using the steps above.** Let me know when you're done or if you encounter any issues!
