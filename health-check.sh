#!/bin/bash
# IntelliStack Railway Health Check Script
# Verifies all services are healthy after deployment

set -e

echo "🏥 IntelliStack Health Check"
echo "============================"
echo ""

# Get Railway service URLs
echo "📡 Fetching service URLs from Railway..."
cd intellistack/backend
BACKEND_URL=$(railway variables --service backend | grep "RAILWAY_PUBLIC_DOMAIN" | cut -d'=' -f2 || echo "")
cd ../auth-server
AUTH_URL=$(railway variables --service auth-server | grep "RAILWAY_PUBLIC_DOMAIN" | cut -d'=' -f2 || echo "")
cd ../content
CONTENT_URL=$(railway variables --service content | grep "RAILWAY_PUBLIC_DOMAIN" | cut -d'=' -f2 || echo "")
cd ../..

if [ -z "$BACKEND_URL" ] || [ -z "$AUTH_URL" ] || [ -z "$CONTENT_URL" ]; then
    echo "⚠️  Could not fetch service URLs automatically"
    echo "Please enter them manually:"
    read -p "Backend URL (e.g., backend-production.up.railway.app): " BACKEND_URL
    read -p "Auth URL (e.g., auth-production.up.railway.app): " AUTH_URL
    read -p "Content URL (e.g., content-production.up.railway.app): " CONTENT_URL
fi

echo ""
echo "Service URLs:"
echo "  Backend: https://$BACKEND_URL"
echo "  Auth:    https://$AUTH_URL"
echo "  Content: https://$CONTENT_URL"
echo ""

# Test Backend Health
echo "🔍 Testing Backend Health..."
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$BACKEND_URL/health" || echo "000")
if [ "$BACKEND_STATUS" = "200" ]; then
    echo "✅ Backend: HEALTHY (200 OK)"
    curl -s "https://$BACKEND_URL/health" | jq '.' || echo ""
else
    echo "❌ Backend: UNHEALTHY (HTTP $BACKEND_STATUS)"
fi
echo ""

# Test Auth Server Health
echo "🔍 Testing Auth Server Health..."
AUTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$AUTH_URL/health" || echo "000")
if [ "$AUTH_STATUS" = "200" ]; then
    echo "✅ Auth Server: HEALTHY (200 OK)"
    curl -s "https://$AUTH_URL/health" | jq '.' || echo ""
else
    echo "❌ Auth Server: UNHEALTHY (HTTP $AUTH_STATUS)"
fi
echo ""

# Test Content Service
echo "🔍 Testing Content Service..."
CONTENT_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$CONTENT_URL/" || echo "000")
if [ "$CONTENT_STATUS" = "200" ]; then
    echo "✅ Content: HEALTHY (200 OK)"
else
    echo "❌ Content: UNHEALTHY (HTTP $CONTENT_STATUS)"
fi
echo ""

# Check Railway logs for errors
echo "🔍 Checking Railway logs for errors..."
echo ""
echo "Backend errors (last 50 lines):"
railway logs --service backend --tail 50 | grep -i "error" || echo "  No errors found"
echo ""
echo "Auth Server errors (last 50 lines):"
railway logs --service auth-server --tail 50 | grep -i "error" || echo "  No errors found"
echo ""
echo "Content errors (last 50 lines):"
railway logs --service content --tail 50 | grep -i "error" || echo "  No errors found"
echo ""

# Summary
echo "📊 Health Check Summary"
echo "======================="
if [ "$BACKEND_STATUS" = "200" ] && [ "$AUTH_STATUS" = "200" ] && [ "$CONTENT_STATUS" = "200" ]; then
    echo "✅ All services are HEALTHY"
    echo ""
    echo "🎉 Deployment successful!"
    echo ""
    echo "Service URLs:"
    echo "  Backend:  https://$BACKEND_URL"
    echo "  Auth:     https://$AUTH_URL"
    echo "  Content:  https://$CONTENT_URL"
    exit 0
else
    echo "❌ Some services are UNHEALTHY"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check Railway logs: railway logs --service <service-name>"
    echo "2. Verify environment variables in Railway dashboard"
    echo "3. Check for build errors in Railway deployment logs"
    echo "4. See DEPLOYMENT_CHECKLIST.md for detailed verification steps"
    exit 1
fi
