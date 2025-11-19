import os
import glob

def count_solutions():
    ratings = ['800', '900', '1000', '1100', '1200', '1300', '1400', '1500', 
               '1600', '1700', '1800', '1900', '2000']
    
    progress = {}
    rating_counts = {}
    
    # Count solutions for each rating
    for rating in ratings:
        cpp_files = glob.glob(f'problems/{rating}/*.cpp')
        py_files = glob.glob(f'problems/{rating}/*.py')
        total = len(cpp_files) + len(py_files)
        
        rating_counts[rating] = total
        
        # Always add to progress, even if 0
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
    # Create rating distribution table
    distribution_table = "## 📈 Rating Distribution\n\n"
    distribution_table += "| Rating | Problems Solved | Progress |\n"
    distribution_table += "|--------|----------------|----------|\n"
    
    for rating in sorted(progress.keys(), key=int):
        count = progress[rating]['total']
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
    coverage_percentage = (solved_ratings / total_possible_ratings) * 100 if total_possible_ratings > 0 else 0
    
    most_solved_rating = max(rating_counts, key=rating_counts.get) if rating_counts.values() and max(rating_counts.values()) > 0 else 'N/A'
    most_solved_count = max(rating_counts.values()) if rating_counts.values() and max(rating_counts.values()) > 0 else 0
    
    readme_content = f"""# 🚀 Codeforces Solutions

![Progress](https://img.shields.io/badge/Solved-{total}-brightgreen)
![C++](https://img.shields.io/badge/C++-{cpp_count}-blue) 
![Python](https://img.shields.io/badge/Python-{py_count}-yellow)
![Coverage](https://img.shields.io/badge/Rating_Coverage-{solved_ratings}/{total_possible_ratings}-orange)

## 🎯 Quick Stats
- **Total Problems Solved**: {total}
- **Rating Coverage**: {solved_ratings}/{total_possible_ratings} ({coverage_percentage:.1f}%)
- **Most Solved Rating**: {most_solved_rating} ({most_solved_count} problems)
- **Languages**: C++ ({cpp_count}), Python ({py_count})

{distribution_table}

{detailed_table}


*Updated automatically - Keep coding! 🚀*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"DEBUG: 800 rating has {progress['800']['total']} problems (C++: {progress['800']['cpp']}, Python: {progress['800']['python']})")

def main():
    if not os.path.exists('problems'):
        os.makedirs('problems')
    
    progress, total, cpp_count, py_count, rating_counts = count_solutions()
    update_readme(progress, total, cpp_count, py_count, rating_counts)
    print(f"✅ Updated README - {total} problems solved across {len([x for x in rating_counts.values() if x > 0])} ratings")

if __name__ == "__main__":
    main()