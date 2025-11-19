import os
import glob

def count_solutions():
    ratings = ['800', '900', '1000', '1100', '1200', '1300', '1400', '1500', 
               '1600', '1700', '1800', '1900', '2000']
    
    progress = {}
    
    for rating in ratings:
        cpp_files = glob.glob(f'problems/{rating}/*.cpp')
        py_files = glob.glob(f'problems/{rating}/*.py')
        total = len(cpp_files) + len(py_files)
        
        if total > 0:
            progress[rating] = {
                'total': total,
                'cpp': len(cpp_files),
                'python': len(py_files)
            }
    
    all_cpp = glob.glob('problems/**/*.cpp', recursive=True)
    all_py = glob.glob('problems/**/*.py', recursive=True)
    total_all = len(all_cpp) + len(all_py)
    
    return progress, total_all, len(all_cpp), len(all_py)

def update_readme(progress, total, cpp_count, py_count):
    readme_content = f"""# 🚀 Codeforces Solutions

![Progress](https://img.shields.io/badge/Solved-{total}-brightgreen)
![C++](https://img.shields.io/badge/C++-{cpp_count}-blue) 
![Python](https://img.shields.io/badge/Python-{py_count}-yellow)

## 📊 Progress Overview

| Rating | Total | C++ | Python |
|--------|-------|-----|--------|
"""
    
    for rating in sorted(progress.keys(), key=int):
        data = progress[rating]
        readme_content += f"| {rating} | {data['total']} | {data['cpp']} | {data['python']} |\n"
    
    readme_content += f"| **Total** | **{total}** | **{cpp_count}** | **{py_count}** |\n\n"
    
    readme_content += """## 🗂️ Folder Structure
codeforces-solutions/
├── problems/
│ ├── 800/ - Rating 800 problems
│ ├── 900/ - Rating 900 problems
│ └── .../
├── scripts/ - Automation scripts
└── README.md - Auto-generated

*Updated automatically*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    if not os.path.exists('problems'):
        os.makedirs('problems')
    
    progress, total, cpp_count, py_count = count_solutions()
    update_readme(progress, total, cpp_count, py_count)
    print(f"✅ Updated README - {total} problems solved")

if __name__ == "__main__":
    main()