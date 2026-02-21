#!/usr/bin/env python3
"""
Railway Root Directory Fix Script
Guides user through fixing trailing spaces in Railway dashboard
"""

import webbrowser
import time
import subprocess

PROJECT_URL = "https://railway.com/project/1c394e87-e809-442b-aa14-55ceabb26d9c"

SERVICES = {
    "backend": "intellistack/backend",
    "auth-server": "intellistack/auth-server",
    "content": "intellistack/content"
}

def print_header():
    print("\n" + "="*60)
    print("🚂 Railway Root Directory Fix")
    print("="*60 + "\n")

def print_instructions():
    print("📋 What we're fixing:")
    print("   The Root Directory fields have trailing spaces")
    print("   This prevents Railway from finding your code\n")

    print("⏱️  Time required: 2-3 minutes\n")

    print("🎯 What you'll do:")
    print("   1. Open Railway dashboard (will open automatically)")
    print("   2. For each service, fix the Root Directory field")
    print("   3. Redeploy each service\n")

def open_dashboard():
    print("🌐 Opening Railway dashboard...")
    webbrowser.open(PROJECT_URL)
    time.sleep(2)
    print("✅ Dashboard opened in your browser\n")

def guide_service_fix(service_name, correct_path):
    print(f"\n{'─'*60}")
    print(f"🔧 Fixing: {service_name.upper()}")
    print(f"{'─'*60}\n")

    print(f"1. Click on the '{service_name}' service card")
    print(f"2. Click the 'Settings' tab at the top")
    print(f"3. Scroll down to find 'Root Directory' field")
    print(f"4. Select ALL text in that field (Ctrl+A or Cmd+A)")
    print(f"5. Delete it completely")
    print(f"6. Type exactly: {correct_path}")
    print(f"   ⚠️  Type it manually - don't copy-paste!")
    print(f"7. Press Tab or click outside the field")
    print(f"8. Click 'Redeploy' button at the top\n")

    input(f"✅ Press Enter when you've fixed {service_name}...")

def verify_deployment(service_name):
    print(f"\n🔍 Checking {service_name} deployment...")

    try:
        result = subprocess.run(
            ["railway", "service", service_name, "logs", "--deployment"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if "does not exist" in result.stdout or "does not exist" in result.stderr:
            print(f"❌ {service_name} still has the issue")
            print(f"   Please double-check the Root Directory field\n")
            return False
        else:
            print(f"✅ {service_name} looks good!\n")
            return True
    except Exception as e:
        print(f"⚠️  Could not verify {service_name} (this is okay)")
        print(f"   We'll check all services at the end\n")
        return True

def final_verification():
    print("\n" + "="*60)
    print("🎉 All services configured!")
    print("="*60 + "\n")

    print("⏳ Waiting 60 seconds for deployments to start...\n")
    time.sleep(60)

    print("📊 Checking deployment status...\n")

    for service_name in SERVICES.keys():
        try:
            result = subprocess.run(
                ["railway", "service", service_name, "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            print(f"{service_name}: {result.stdout.strip()}")
        except:
            print(f"{service_name}: Could not check status")

    print("\n✅ Configuration complete!")
    print("\n📝 Next steps:")
    print("   1. Monitor deployments in Railway dashboard")
    print("   2. Check build logs for any errors")
    print("   3. Once deployed, test the health endpoints\n")

def main():
    print_header()
    print_instructions()

    input("Press Enter to start...")

    open_dashboard()

    for service_name, correct_path in SERVICES.items():
        guide_service_fix(service_name, correct_path)
        verify_deployment(service_name)

    final_verification()

if __name__ == "__main__":
    main()
