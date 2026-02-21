#!/bin/bash
# Railway Service Configuration Script
# This script configures the root directory for each service via Railway dashboard

echo "🚂 Railway Service Configuration"
echo ""
echo "Unfortunately, the Railway CLI doesn't support setting root directories for monorepo services."
echo "You need to configure this through the Railway dashboard."
echo ""
echo "📋 Quick Configuration Steps:"
echo ""
echo "1. Open Railway Dashboard:"
echo "   https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c"
echo ""
echo "2. For BACKEND service:"
echo "   - Click on 'backend' service"
echo "   - Click 'Settings' tab"
echo "   - Under 'Source' section, find 'Root Directory'"
echo "   - Enter: intellistack/backend"
echo "   - Click 'Save'"
echo "   - Click 'Deploy' button"
echo ""
echo "3. For AUTH-SERVER service:"
echo "   - Click on 'auth-server' service"
echo "   - Click 'Settings' tab"
echo "   - Under 'Source' section, find 'Root Directory'"
echo "   - Enter: intellistack/auth-server"
echo "   - Click 'Save'"
echo "   - Click 'Deploy' button"
echo ""
echo "4. For CONTENT service:"
echo "   - Click on 'content' service"
echo "   - Click 'Settings' tab"
echo "   - Under 'Source' section, find 'Root Directory'"
echo "   - Enter: intellistack/content"
echo "   - Click 'Save'"
echo "   - Click 'Deploy' button"
echo ""
echo "⏱️  This will take about 2 minutes to configure all services."
echo ""
echo "✅ After configuration, your services will deploy successfully!"
echo ""
echo "Press any key to open the Railway dashboard..."
read -n 1 -s

# Open Railway dashboard
if command -v xdg-open > /dev/null; then
    xdg-open "https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c"
elif command -v open > /dev/null; then
    open "https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c"
elif command -v start > /dev/null; then
    start "https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c"
else
    echo "Please open this URL manually:"
    echo "https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c"
fi
