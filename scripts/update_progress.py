import os
import glob

def count_solutions():
    ratings = ['800', '900', '1000', '1100', '1200', '1300', '1400', '1500', 
               '1600', '1700', '1800', '1900', '2000']
    
    progress = {}
    rating_counts = {}
    
    # Initialize all ratings to 0
    for rating in ratings:
        rating_counts[rating] = 0
    
    # Count solutions for each rating
    for rating in ratings:
        cpp_files = glob.glob(f'problems/{rating}/*.cpp')
        py_files = glob.glob(f'problems/{rating}/*.py')
        total = len(cpp_files) + len(py_files)
        
        rating_counts[rating] = total
        
        if total > 0:
            progress[rating] = {
                'total': total,
                'cpp': len(cpp_files),
                'python': len(py_files)
            }
    
    # Total counts
    all_cpp = glob.glob('problems/**/*.cpp', recursive=True)
    all_py = glob.glob('problems/**/*.py', recursive=True)
    total_all = len(all_cpp) + len(all_py)
    
    return progress, total_all, len(all_cpp), len(all_py), rating_counts

def update_readme(progress, total, cpp_count, py_count, rating_counts):
    # Create progress bar for each rating
    progress_bars = ""
    max_problems = max(rating_counts.values()) if rating_counts.values() else 1
    
    for rating in sorted(rating_counts.keys(), key=int):
        count = rating_counts[rating]
        if max_problems > 0:
            percentage = (count / max_problems) * 100
            bars = "█" * int(percentage / 10) + "░" * (10 - int(percentage / 10))
        else:
            bars = "░░░░░░░░░░"
        
        progress_bars += f"**{rating}**: {bars} {count} problems\n"
    
    # Create rating distribution table
    distribution_table = "## 📈 Rating Distribution\n\n"
    distribution_table += "| Rating | Problems Solved | Progress |\n"
    distribution_table += "|--------|----------------|----------|\n"
    
    for rating in sorted(rating_counts.keys(), key=int):
        count = rating_counts[rating]
        progress_bar = "█" * min(count, 10) + "░" * (10 - min(count, 10))
        distribution_table += f"| {rating} | {count} | {progress_bar} |\n"
    
    # Create detailed breakdown table
    detailed_table = "## 📊 Detailed Breakdown\n\n"
    detailed_table += "| Rating | Total | C++ | Python | Completion |\n"
    detailed_table += "|--------|-------|-----|--------|------------|\n"
    
    for rating in sorted(progress.keys(), key=int):
        data = progress[rating]
        completion = "⭐" * min(data['total'], 5) + "○" * (5 - min(data['total'], 5))
        detailed_table += f"| {rating} | {data['total']} | {data['cpp']} | {data['python']} | {completion} |\n"
    
    detailed_table += f"| **Total** | **{total}** | **{cpp_count}** | **{py_count}** | **{total} problems** |\n\n"
    
    # Calculate some stats
    solved_ratings = len([count for count in rating_counts.values() if count > 0])
    total_possible_ratings = len(rating_counts)
    coverage_percentage = (solved_ratings / total_possible_ratings) * 100
    
    readme_content = f"""# 🚀 Codeforces Solutions

![Progress](https://img.shields.io/badge/Solved-{total}-brightgreen)
![C++](https://img.shields.io/badge/C++-{cpp_count}-blue) 
![Python](https://img.shields.io/badge/Python-{py_count}-yellow)
![Coverage](https://img.shields.io/badge/Rating_Coverage-{solved_ratings}/{total_possible_ratings}-orange)

## 🎯 Quick Stats
- **Total Problems Solved**: {total}
- **Rating Coverage**: {solved_ratings}/{total_possible_ratings} ({coverage_percentage:.1f}%)
- **Most Solved Rating**: {max(rating_counts, key=rating_counts.get) if rating_counts.values() else 'N/A'} ({max(rating_counts.values()) if rating_counts.values() else 0} problems)
- **Languages**: C++ ({cpp_count}), Python ({py_count})

{distribution_table}

{detailed_table}

## 📁 Folder Structure
codeforces-solutions/
├── problems/
│ ├── 800/ - {rating_counts['800']} problems
│ ├── 900/ - {rating_counts['900']} problems
│ ├── 1000/ - {rating_counts['1000']} problems
│ ├── 1100/ - {rating_counts['1100']} problems
│ ├── 1200/ - {rating_counts['1200']} problems
│ └── .../
├── scripts/ - Automation scripts
└── README.md - Auto-generated

*Updated automatically - Keep coding! 🚀*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    if not os.path.exists('problems'):
        os.makedirs('problems')
    
    progress, total, cpp_count, py_count, rating_counts = count_solutions()
    update_readme(progress, total, cpp_count, py_count, rating_counts)
    print(f"✅ Updated README - {total} problems solved across {len([x for x in rating_counts.values() if x > 0])} ratings")

if __name__ == "__main__":
    main()