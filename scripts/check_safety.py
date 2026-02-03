"""
Safety Check Script for FRIDAY
Verifies no sensitive data will be committed to Git
"""

import os
import subprocess
from pathlib import Path


def check_gitignore():
    """Check if .gitignore exists and contains necessary entries"""
    print("🔍 Checking .gitignore...")
    
    if not Path('.gitignore').exists():
        print("  ❌ .gitignore file is missing!")
        return False
    
    with open('.gitignore') as f:
        gitignore_content = f.read()
    
    required_entries = ['.env', '__pycache__', '.venv', '*.pyc']
    missing = []
    
    for entry in required_entries:
        if entry not in gitignore_content:
            missing.append(entry)
    
    if missing:
        print(f"  ⚠️  .gitignore missing entries: {', '.join(missing)}")
        return False
    
    print("  ✅ .gitignore looks good")
    return True


def check_env_not_tracked():
    """Check if .env is not being tracked by git"""
    print("\n🔍 Checking if .env is tracked by git...")
    
    try:
        result = subprocess.run(
            ['git', 'ls-files'],
            capture_output=True,
            text=True,
            check=True
        )
        
        tracked_files = result.stdout
        
        if '.env' in tracked_files or '.env.json' in tracked_files:
            print("  ❌ DANGER! .env or .env.json is being tracked by git!")
            print("  Run: git rm --cached .env")
            return False
        
        print("  ✅ .env is not tracked")
        return True
        
    except subprocess.CalledProcessError:
        print("  ⚠️  Not a git repository or git not installed")
        return True
    except FileNotFoundError:
        print("  ⚠️  Git not found in system PATH")
        return True


def check_hardcoded_keys():
    """Check for hardcoded API keys in Python files"""
    print("\n🔍 Scanning for hardcoded API keys...")
    
    found_issues = []
    
    for py_file in Path('.').rglob('*.py'):
        # Skip virtual environment and cache
        if '.venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
        
        # Skip this check script itself
        if py_file.name == 'check_safety.py':
            continue
        
        try:
            with open(py_file, encoding='utf-8') as f:
                content = f.read()
            
            # Check for OpenAI API key pattern
            if 'sk-proj-' in content or 'sk-' in content:
                # Make sure it's not in a comment or example
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if ('sk-proj-' in line or 'sk-' in line) and not line.strip().startswith('#'):
                        if 'your-' not in line and 'example' not in line.lower():
                            found_issues.append(f"  ⚠️  {py_file}:{i} - Possible OpenAI key")
            
            # Check for hardcoded api_key assignments
            if 'api_key="' in content or "api_key='" in content:
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if ('api_key="' in line or "api_key='" in line):
                        if 'os.getenv' not in line and '#' not in line[:line.find('api_key')]:
                            found_issues.append(f"  ⚠️  {py_file}:{i} - Hardcoded api_key")
        
        except Exception as e:
            print(f"  ⚠️  Could not scan {py_file}: {e}")
    
    if found_issues:
        print("  ❌ Found potential hardcoded keys:")
        for issue in found_issues:
            print(issue)
        return False
    
    print("  ✅ No hardcoded keys found")
    return True


def check_env_example_exists():
    """Check if .env.example exists"""
    print("\n🔍 Checking for .env.example...")
    
    if not Path('.env.example').exists():
        print("  ⚠️  .env.example file not found")
        print("  Users won't know what to configure")
        return False
    
    print("  ✅ .env.example exists")
    return True


def check_required_files():
    """Check if all required documentation exists"""
    print("\n🔍 Checking required files...")
    
    required = {
        'README.md': 'Main documentation',
        'requirements.txt': 'Python dependencies',
        '.gitignore': 'Git ignore rules'
    }
    
    all_good = True
    for file, description in required.items():
        if Path(file).exists():
            print(f"  ✅ {file} - {description}")
        else:
            print(f"  ❌ {file} missing - {description}")
            all_good = False
    
    return all_good


def main():
    """Run all safety checks"""
    print("=" * 60)
    print("🛡️  FRIDAY SAFETY CHECK")
    print("=" * 60)
    
    checks = [
        check_gitignore(),
        check_env_not_tracked(),
        check_hardcoded_keys(),
        check_env_example_exists(),
        check_required_files()
    ]
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print("✅ ALL SAFETY CHECKS PASSED!")
        print("🚀 Safe to commit and push to GitHub")
        return True
    else:
        print("❌ SAFETY ISSUES FOUND!")
        print("⚠️  FIX ISSUES BEFORE PUSHING TO GITHUB!")
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
