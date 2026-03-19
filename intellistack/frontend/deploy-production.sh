#!/bin/bash
# Production deployment script for IntelliStack Frontend to Netlify

set -e

echo "🚀 IntelliStack Frontend - Production Deployment"
echo "================================================"
echo ""

# Check if netlify CLI is installed
if ! command -v netlify &> /dev/null; then
    echo "❌ Netlify CLI not found. Install with: npm install -g netlify-cli"
    exit 1
fi

# Set environment variables for Netlify
echo "📝 Setting Netlify environment variables..."
netlify env:set NEXT_PUBLIC_AUTH_URL "" --context production
netlify env:set NEXT_PUBLIC_API_URL "" --context production
netlify env:set NEXT_PUBLIC_DOCUSAURUS_URL "https://saramali15792.github.io/AINativeBook/" --context production

echo "✅ Environment variables set"
echo ""

# Build the application
echo "🔨 Building Next.js application..."
npm run build

echo "✅ Build complete"
echo ""

# Deploy to Netlify
echo "🌐 Deploying to Netlify..."
netlify deploy --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🔗 Frontend: https://intellistack-frontend.netlify.app"
echo "🔗 Auth Server: https://auth-server-production-0f46.up.railway.app"
echo "🔗 Backend API: https://backend-production-bcb8.up.railway.app"
echo "🔗 Documentation: https://saramali15792.github.io/AINativeBook/"
echo ""
echo "⚠️  IMPORTANT: Update Railway environment variables:"
echo ""
echo "Auth Server CORS_ORIGINS:"
echo "  https://intellistack-frontend.netlify.app,https://saramali15792.github.io,https://backend-production-bcb8.up.railway.app"
echo ""
echo "Backend CORS_ORIGINS:"
echo "  https://intellistack-frontend.netlify.app,https://saramali15792.github.io,https://auth-server-production-0f46.up.railway.app,https://backend-production-bcb8.up.railway.app"
echo ""
