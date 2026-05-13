#!/usr/bin/env python3
"""
طرّة Installation Verification Script
Checks that everything is set up correctly before running
"""

import os
import sys
import subprocess

def check_python_version():
    """Check Python version"""
    print("\n📌 Checking Python Version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ✗ Python {version.major}.{version.minor} - FAILED (need 3.7+)")
        return False

def check_pip():
    """Check if pip is available"""
    print("\n📌 Checking pip...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ pip found: {result.stdout.strip()}")
            return True
    except:
        pass
    print("   ✗ pip not found")
    return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📌 Checking Installed Packages...")
    required = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'werkzeug': 'Werkzeug',
        'dateutil': 'python-dateutil',
        'PIL': 'Pillow',
        'reportlab': 'ReportLab',
        'openpyxl': 'openpyxl',
        'qrcode': 'qrcode',
    }
    
    missing = []
    for module, package_name in required.items():
        try:
            __import__(module)
            print(f"   ✓ {package_name}")
        except ImportError:
            print(f"   ✗ {package_name} - MISSING")
            missing.append(package_name)
    
    return len(missing) == 0, missing

def check_files():
    """Check if all required files exist"""
    print("\n📌 Checking Required Files...")
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/login.html',
        'templates/base.html',
        'templates/dashboard.html',
        'templates/inventory.html',
        'templates/sales.html',
        'templates/services.html',
        'templates/reports.html',
        'templates/settings.html',
    ]
    
    missing = []
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"   ✓ {filepath}")
        else:
            print(f"   ✗ {filepath} - MISSING")
            missing.append(filepath)
    
    return len(missing) == 0, missing

def check_directories():
    """Check and create necessary directories"""
    print("\n📌 Checking Directories...")
    required_dirs = ['instance', 'uploads', 'backups', 'templates']
    
    for dirname in required_dirs:
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
                print(f"   ✓ Created: {dirname}")
            except:
                print(f"   ✗ Failed to create: {dirname}")
                return False
        else:
            print(f"   ✓ {dirname}")
    
    return True

def check_port():
    """Check if port 5000 is available"""
    print("\n📌 Checking Port 5000...")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result != 0:
            print("   ✓ Port 5000 is available")
            return True
        else:
            print("   ⚠ Port 5000 is in use (you can change it in app.py)")
            return True  # Still OK, just warning
    except:
        return True

def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("  طرّة (Tarrah) Installation Verification")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version()),
        ("pip Package Manager", check_pip()),
    ]
    
    # Check dependencies
    deps_ok, missing_deps = check_dependencies()
    checks.append(("Required Packages", deps_ok))
    
    # Check files
    files_ok, missing_files = check_files()
    checks.append(("Required Files", files_ok))
    
    # Check directories
    dirs_ok = check_directories()
    checks.append(("Directories", dirs_ok))
    
    # Check port
    port_ok = check_port()
    checks.append(("Port 5000", port_ok))
    
    # Summary
    print("\n" + "="*60)
    print("  VERIFICATION SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    for check_name, result in checks:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {check_name:<30} {status}")
    
    print("\n" + "="*60)
    print(f"  Result: {passed}/{total} checks passed")
    print("="*60 + "\n")
    
    # Recommendations
    if missing_deps:
        print("📌 MISSING PACKAGES")
        print("   Run this command to install:")
        print(f"   pip install -r requirements.txt\n")
    
    if missing_files:
        print("📌 MISSING FILES")
        print("   The following files are missing:")
        for f in missing_files:
            print(f"   - {f}")
        print("   Make sure you have all project files.\n")
    
    # Final status
    if passed == total:
        print("✓ All checks passed! You're ready to run:")
        print("   python app.py\n")
        print("   Then open: http://localhost:5000")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("   Then run this script again.\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
