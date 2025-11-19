import os
import glob

def count_solutions():
    ratings = ['800', '900', '1000', '1100', '1200', '1300', '1400', '1500', 
               '1600', '1700', '1800', '1900', '2000']
    
    progress = {}
    
    # Count solutions for each rating
    for rating in ratings:
        rating_path = f'problems/{rating}'
        if not os.path.exists(rating_path):
            progress[rating] = {'total': 0, 'cpp': 0, 'python': 0}
            continue
            
        # Get all problem folders in this rating
        problem_folders = [f for f in os.listdir(rating_path) 
                          if os.path.isdir(os.path.join(rating_path, f))]
        
        cpp_count = 0
        python_count = 0
        
        # Check each problem folder for solution files
        for problem_folder in problem_folders:
            problem_path = os.path.join(rating_path, problem_folder)
            
            # Check for C++ files (main.cpp or any .cpp file)
            cpp_files = glob.glob(os.path.join(problem_path, '*.cpp')) + \
                       glob.glob(os.path.join(problem_path, 'main.cpp'))
            
            # Check for Python files (main.py or any .py file)  
            py_files = glob.glob(os.path.join(problem_path, '*.py')) + \
                      glob.glob(os.path.join(problem_path, 'main.py'))
            
            if cpp_files:
                cpp_count += 1
            if py_files:
                python_count += 1
        
        total_problems = len(problem_folders)
        progress[rating] = {
            'total': total_problems,
            'cpp': cpp_count,
            'python': python_count
        }
    
    # Calculate totals
    total_all = sum(data['total'] for data in progress.values())
    cpp_total = sum(data['cpp'] for data in progress.values())
    py_total = sum(data['python'] for data in progress.values())
    
    return progress, total_all, cpp_total, py_total

def update_readme(progress, total, cpp_count, py_count):
    # Create detailed breakdown table - ONLY show ratings that have problems
    detailed_table = "## 📊 Solutions Breakdown\n\n"
    detailed_table += "| Rating | Problems | C++ | Python |\n"
    detailed_table += "|--------|----------|-----|--------|\n"
    
    has_problems = False
    for rating in sorted(progress.keys(), key=int):
        data = progress[rating]
        if data['total'] > 0:
            detailed_table += f"| {rating} | {data['total']} | {data['cpp']} | {data['python']} |\n"
            has_problems = True
    
    if not has_problems:
        detailed_table += "| No problems solved yet! | | | |\n"
    
    detailed_table += f"| **Total** | **{total}** | **{cpp_count}** | **{py_count}** |\n\n"
    
    # Calculate stats
    solved_ratings = len([data for data in progress.values() if data['total'] > 0])
    total_possible_ratings = len(progress)
    
    readme_content = f"""# 🚀 Codeforces Solutions

![Progress](https://img.shields.io/badge/Solved-{total}-brightgreen)
![C++](https://img.shields.io/badge/C++-{cpp_count}-blue) 
![Python](https://img.shields.io/badge/Python-{py_count}-yellow)

## 🎯 Quick Stats
- **Total Problems Solved**: {total}
- **Rating Coverage**: {solved_ratings}/{total_possible_ratings} ratings

{detailed_table}

*Updated automatically*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Debug print
    print(f"DEBUG: Found {total} total problems:")
    for rating in sorted(progress.keys(), key=int):
        data = progress[rating]
        if data['total'] > 0:
            print(f"  Rating {rating}: {data['total']} problems ({data['cpp']} C++, {data['python']} Python)")

def main():
    if not os.path.exists('problems'):
        os.makedirs('problems')
    
    progress, total, cpp_count, py_count = count_solutions()
    update_readme(progress, total, cpp_count, py_count)
    print(f"✅ Updated README - {total} problems solved")

if __name__ == "__main__":
    main()