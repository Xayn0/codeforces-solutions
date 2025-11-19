import os
import glob

def main():
    # Count all solution files
    cpp_files = glob.glob('problems/**/*.cpp', recursive=True)
    py_files = glob.glob('problems/**/*.py', recursive=True)
    total = len(cpp_files) + len(py_files)
    
    # Create README content
    readme = f"""# Codeforces Solutions

## 📊 Progress
**Total Problems Solved:** {total}
**C++:** {len(cpp_files)}
**Python:** {len(py_files)}

## 🗂️ Structure
- `problems/800/` - Easy problems
- `problems/900/` - 
- `problems/1000/` - 
- ...etc

*Last updated automatically*
"""
    
    # Write README
    with open('README.md', 'w') as f:
        f.write(readme)
    
    print(f"✅ Updated README - {total} problems solved")

if __name__ == "__main__":
    main()