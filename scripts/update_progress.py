import os
import glob
import requests
import json

def get_codeforces_rating(handle):
    """Fetch current rating from Codeforces API"""
    try:
        url = f"https://codeforces.com/api/user.info?handles={handle}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if data['status'] == 'OK' and data['result']:
            user_info = data['result'][0]
            rating = user_info.get('rating', 'Unrated')
            max_rating = user_info.get('maxRating', 'Unrated')
            rank = user_info.get('rank', 'Unrated')
            return rating, max_rating, rank
        else:
            return 'Unrated', 'Unrated', 'Unrated'
    except:
        return 'Unrated', 'Unrated', 'Unrated'

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
    
    # Calculate totals and average rating
    total_all = sum(data['total'] for data in progress.values())
    cpp_total = sum(data['cpp'] for data in progress.values())
    py_total = sum(data['python'] for data in progress.values())
    
    # Calculate weighted average rating
    total_weighted = 0
    total_problems_for_avg = 0
    for rating, data in progress.items():
        if data['total'] > 0:
            total_weighted += int(rating) * data['total']
            total_problems_for_avg += data['total']
    
    avg_rating = round(total_weighted / total_problems_for_avg) if total_problems_for_avg > 0 else 0
    
    return progress, total_all, cpp_total, py_total, avg_rating

def update_readme(progress, total, cpp_count, py_count, avg_rating, cf_rating, cf_max_rating, cf_rank):
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
    
    # Codeforces rating badge
    rating_color = "red"
    if cf_rating != 'Unrated':
        rating_num = int(cf_rating)
        if rating_num < 1200:
            rating_color = "gray"
        elif rating_num < 1400:
            rating_color = "green"
        elif rating_num < 1600:
            rating_color = "cyan"
        elif rating_num < 1900:
            rating_color = "blue"
        elif rating_num < 2100:
            rating_color = "violet"
        elif rating_num < 2400:
            rating_color = "orange"
        else:
            rating_color = "red"
    
    readme_content = f"""# 🚀 Codeforces Solutions

![Progress](https://img.shields.io/badge/Solved-{total}-brightgreen)
![C++](https://img.shields.io/badge/C++-{cpp_count}-blue) 
![Python](https://img.shields.io/badge/Python-{py_count}-yellow)
![Avg Rating](https://img.shields.io/badge/Average_Rating-{avg_rating}-orange)
![CF Rating](https://img.shields.io/badge/Codeforces-{cf_rating}-{rating_color})

## 🎯 Quick Stats
- **Total Problems Solved**: {total}
- **Average Problem Rating**: {avg_rating}
- **Rating Coverage**: {solved_ratings}/{total_possible_ratings} ratings
- **Codeforces Handle**: [thehandsomeone](https://codeforces.com/profile/thehandsomeone)
- **Current Rating**: {cf_rating} ({cf_rank})
- **Max Rating**: {cf_max_rating}

{detailed_table}

*Updated automatically - Live rating from Codeforces API*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Debug print
    print(f"DEBUG: Found {total} total problems, average rating: {avg_rating}")
    print(f"DEBUG: Codeforces rating: {cf_rating} (Max: {cf_max_rating}, Rank: {cf_rank})")
    for rating in sorted(progress.keys(), key=int):
        data = progress[rating]
        if data['total'] > 0:
            print(f"  Rating {rating}: {data['total']} problems ({data['cpp']} C++, {data['python']} Python)")

def main():
    if not os.path.exists('problems'):
        os.makedirs('problems')
    
    # Get Codeforces rating
    cf_rating, cf_max_rating, cf_rank = get_codeforces_rating('thehandsomeone')
    
    progress, total, cpp_count, py_count, avg_rating = count_solutions()
    update_readme(progress, total, cpp_count, py_count, avg_rating, cf_rating, cf_max_rating, cf_rank)
    print(f"✅ Updated README - {total} problems solved, Average rating: {avg_rating}")

if __name__ == "__main__":
    main()