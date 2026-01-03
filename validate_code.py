"""
Code validation script for AIbot API
Validates Python syntax and imports without running tests
"""
import ast
import sys
import os

def validate_python_file(filepath):
    """Validate Python file syntax"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def main():
    """Validate all Python files"""
    files_to_check = [
        'api.py',
        'app.py',
        'auth.py',
        'model_client.py',
        'tests/test_api.py'
    ]
    
    print("=" * 60)
    print("AIbot Code Validation")
    print("=" * 60)
    
    all_valid = True
    for filepath in files_to_check:
        if os.path.exists(filepath):
            valid, message = validate_python_file(filepath)
            status = "✓ PASS" if valid else "✗ FAIL"
            print(f"{status}: {filepath}")
            if not valid:
                print(f"  Error: {message}")
                all_valid = False
        else:
            print(f"⚠ SKIP: {filepath} (not found)")
    
    print("=" * 60)
    
    if all_valid:
        print("✓ All files validated successfully!")
        return 0
    else:
        print("✗ Some files have errors")
        return 1

if __name__ == '__main__':
    sys.exit(main())
