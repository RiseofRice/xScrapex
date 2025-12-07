"""
Setup script for xScrapex - Twitter/X Scraper
Run this to verify installation and dependencies.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is adequate."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("✗ Python 3.7 or higher is required")
        return False
    
    print("✓ Python version OK")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    required = ['requests', 'bs4', 'colorama']
    missing = []
    
    for module in required:
        try:
            __import__(module)
            print(f"✓ {module} is installed")
        except ImportError:
            print(f"✗ {module} is NOT installed")
            missing.append(module)
    
    return len(missing) == 0, missing


def check_windows_notifications():
    """Check if Windows notification support is available."""
    if sys.platform != 'win32':
        print("⚠ Not running on Windows - native notifications not available")
        return True
    
    try:
        import win10toast
        print("✓ win10toast is installed (Windows notifications enabled)")
        return True
    except ImportError:
        print("⚠ win10toast is NOT installed (notifications will be console-only)")
        print("  Install with: pip install win10toast")
        return False


def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("\nInstalling dependencies from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False


def main():
    """Main setup function."""
    print("="*60)
    print("xScrapex Setup & Verification")
    print("="*60)
    print()
    
    # Check Python version
    if not check_python_version():
        return 1
    
    print()
    
    # Check dependencies
    deps_ok, missing = check_dependencies()
    
    if not deps_ok:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        response = input("Would you like to install them now? (y/n): ")
        
        if response.lower() in ['y', 'yes']:
            if not install_dependencies():
                return 1
        else:
            print("\nPlease install dependencies manually:")
            print("  pip install -r requirements.txt")
            return 1
    
    print()
    
    # Check Windows notifications
    check_windows_notifications()
    
    print()
    print("="*60)
    print("Setup complete! ✓")
    print("="*60)
    print()
    print("To start monitoring a user:")
    print("  python xscrapex.py username")
    print()
    print("For help:")
    print("  python xscrapex.py --help")
    print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
