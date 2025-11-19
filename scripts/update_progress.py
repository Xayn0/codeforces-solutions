import os
import glob

def count_solutions():
    ratings = ['800', '900', '1000', '1100', '1200', '1300', '1400', '1500', 
               '1600', '1700', '1800', '1900', '2000']
    
    progress = {}
    
    # Count solutions for each rating
    for rating in ratings:
        cpp_files = glob.glob(f'problems/{rating}/*.cpp')
        cbp_files = glob.glob(f'problems/{rating}/*.cbp')  # Code::Blocks projects
        py_files = glob.glob(f'problems/{rating}/*.py')
        total = len(cpp_files) + len(cbp_files) + len(py_files)
        
        progress[rating] = {
            'total': total,
            'cpp': len(cpp_files) + len(cbp_files),  # Count both .cpp and .cbp as C++
            'cbp': len(cbp_files),  # Track .cbp separately
            'python': len(py_files)
        }
    
    # Total counts
    all_cpp = glob.glob('problems/**/*.cpp', recursive=True)
    all_cbp = glob.glob('problems/**/*.cbp', recursive=True)  # Code::Blocks files
    all_py = glob.glob('problems/**/*.py', recursive=True)
    total_all = len(all_cpp) + len(all_cbp) + len(all_py)
    
    return progress, total_all, len(all_cpp) + len(all_cbp), len(all_py)

def update_readme(progress, total, cpp_count, py_count):
    # Create detailed breakdown table
    detailed_table = "## 📊 Solutions Breakdown\n\n"
    detailed_table += "| Rating | Total | C++/.cbp | Python |\n"
    detailed_table += "|--------|-------|----------|--------|\n"
    
    for rating in sorted(progress.keys(), key=int):
        data = progress[rating]
        detailed_table += f"| {rating} | {data['total']} | {data['cpp']} | {data['python']} |\n"
    
    detailed_table += f"| **Total** | **{total}** | **{cpp_count}** | **{py_count}** |\n\n"
    
    # Calculate stats
    solved_ratings = len([data for data in progress.values() if data['total'] > 0])
    total_possible_ratings = len(progress)
    coverage_percentage = (solved_ratings / total_possible_ratings) * 100
    
    # Find most solved rating
    most_solved_rating = 'N/A'
    most_solved_count = 0
    for rating, data in progress.items():
        if data['total'] > most_solved_count:
            most_solved_count = data['total']
            most_solved_rating = rating
    
    readme_content = f"""# 🚀 Codeforces Solutions

![Progress](https://img.shields.io/badge/Solved-{total}-brightgreen)
![C++](https://img.shields.io/badge/C++-{cpp_count}-blue) 
![Python](https://img.shields.io/badge/Python-{py_count}-yellow)

## 🎯 Quick Stats
- **Total Problems Solved**: {total}
- **Rating Coverage**: {solved_ratings}/{total_possible_ratings} ratings
- **Most Solved Rating**: {most_solved_rating} ({most_solved_count} problems)
- **File Types**: {cpp_count} C++ (.cpp/.cbp), {py_count} Python

{detailed_table}

## 📁 Folder Structure
codeforces-solutions/
├── problems/
│ ├── 800/ - {progress['800']['total']} problems
│ ├── 900/ - {progress['900']['total']} problems
│ ├── 1000/ - {progress['1000']['total']} problems
│ └── .../
├── scripts/ - Automation scripts
└── README.md - Auto-generated

*Updated automatically - Keep coding! 🚀*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"DEBUG: Found {progress['800']['total']} problems in 800 rating (.cpp: {len(glob.glob('problems/800/*.cpp'))}, .cbp: {len(glob.glob('problems/800/*.cbp'))}, .py: {len(glob.glob('problems/800/*.py'))})")

def main():
    if not os.path.exists('problems'):
        os.makedirs('problems')
        print("Created problems directory")
    
    # Create rating directories if they don't exist
    for rating in ['800', '900', '1000', '1100', '1200', '1300', '1400', '1500', 
                   '1600', '1700', '1800', '1900', '2000']:
        os.makedirs(f'problems/{rating}', exist_ok=True)
    
    progress, total, cpp_count, py_count = count_solutions()
    update_readme(progress, total, cpp_count, py_count)
    print(f"✅ Updated README - {total} problems solved")

if __name__ == "__main__":
    main()