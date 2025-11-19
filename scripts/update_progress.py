import os
import glob

def count_solutions():
    print("🔍 Scanning for solution files...")
    
    # Count files in each rating folder
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
        print(f"Rating {rating}: {total} files")
    
    # Total counts
    all_cpp = glob.glob('problems/**/*.cpp', recursive=True)
    all_py = glob.glob('problems/**/*.py', recursive=True)
    total_all = len(all_cpp) + len(all_py)
    
    print(f"📊 Total solutions found: {total_all}")
    return progress, total_all, len(all_cpp), len(all_py)

def update_readme(progress, total, cpp_count, py_count):
    # Create the README content
    readme_content = f"""# 🚀 Codeforces Solutions

![Progress](https://img.shields.io/badge/Solved-{total}-brightgreen)
![C++](https://img.shields.io/badge/C++-{cpp_count}-blue) 
![Python](https://img.shields.io/badge/Python-{py_count}-yellow)

## 📊 Progress Overview

| Rating | Total | C++ | Python |
|--------|-------|-----|--------|
"""
    
    # Add rows for each rating that has solutions
    for rating in sorted(progress.keys(), key=int):
        data = progress[rating]
        readme_content += f"| {rating} | {data['total']} | {data['cpp']} | {data['python']} |\n"
    
    readme_content += f"| **Total** | **{total}** | **{cpp_count}** | **{py_count}** |\n\n"
    
    readme_content += """## 🗂️ Folder Structure