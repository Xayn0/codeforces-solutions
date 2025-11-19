import os
import glob
import urllib.request
import json

def get_codeforces_rating(handle):
    """Fetch current rating from Codeforces API using urllib (no extra modules needed)"""
    try:
        url = f"https://codeforces.com/api/user.info?handles={handle}"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if data['status'] == 'OK' and data['result']:
                user_info = data['result'][0]
                rating = user_info.get('rating', 'Unrated')
                max_rating = user_info.get('maxRating', 'Unrated')
                rank = user_info.get('rank', 'Unrated')
                return rating, max_rating, rank
    except:
        pass
    return 'Unrated', 'Unrated', 'Unrated'

def count_solutions():
    ratings = ['800', '900', '1000', '1100', '1200', '1300', '1400', '1500', 
               '1600', '1700', '1800', '1900', '2000']
    
    progress = {}
    
    # Count solutions for each rating
    for rating in ratings:
        rating_path = f'problems/{rating}'
        if not os.path.exists(rating_path):
            progress[rating] = {'total': 0}
            continue
            
        # Get all problem folders in this rating
        problem_folders = [f for f in os.listdir(rating_path) 
                          if os.path.isdir(os.path.join(rating_path, f))]
        
        solved_count = 0
        
        # Check each problem folder for C++ files
        for problem_folder in problem_folders:
            problem_path = os.path.join(rating_path, problem_folder)
            
            # Check for C++ files (main.cpp or any .cpp file)
            cpp_files = glob.glob(os.path.join(problem_path, '*.cpp')) + \
                       glob.glob(os.path.join(problem_path, 'main.cpp'))
            
            if cpp_files:
                solved_count += 1
        
        progress[rating] = {'total': solved_count}
    
    # Calculate totals and average rating
    total_all = sum(data['total'] for data in progress.values())
    
    # Calculate weighted average rating
    total_weighted = 0
    total_problems_for_avg = 0
    for rating, data in progress.items():
        if data['total'] > 0:
            total_weighted += int(rating) * data['total']
            total_problems_for_avg += data['total']
    
    avg_rating = round(total_weighted / total_problems_for_avg) if total_problems_for_avg > 0 else 0
    
    return progress, total_all, avg_rating

def update_readme(progress, total, avg_rating, cf_rating, cf_max_rating, cf_rank):
    # Create detailed breakdown table - ONLY show ratings that have problems
    detailed_table = "## 📊 Solutions Breakdown\n\n"
    detailed_table += "| Rating | Problems Solved |\n"
    detailed_table += "|--------|----------------|\n"
    
    has_problems = False
    for rating in sorted(progress.keys(), key=int):
        data = progress[rating]
        if data['total'] > 0:
            detailed_table += f"| {rating} | {data['total']} |\n"
            has_problems = True
    
    if not has_problems:
        detailed_table += "| No problems solved yet! |\n"
    
    detailed_table += f"| **Total** | **{total}** |\n\n"
    
    # Calculate stats
    solved_ratings = len([data for data in progress.values() if data['total'] > 0])
    total_possible_ratings = len(progress)
    
    # Codeforces rating section
    if cf_rating != 'Unrated':
        cf_section = f"""
## 🏆 Codeforces Profile

**Handle**: [thehandsomeone](https://codeforces.com/profile/thehandsomeone)  
**Current Rating**: {cf_rating} ({cf_rank})  
**Max Rating**: {cf_max_rating}
"""
    else:
        cf_section = """
## 🏆 Codeforces Profile

**Handle**: [thehandsomeone](https://codeforces.com/profile/thehandsomeone)  
**Status**: Rating not available
"""
    
    readme_content = f"""# 🚀 Codeforces Solutions

![Progress](https://img.shields.io/badge/Solved-{total}-brightgreen)
![C++](https://img.shields.io/badge/Language-C++-blue)
![Avg Rating](https://img.shields.io/badge/Average_Rating-{avg_rating}-orange)

## 📈 Progress Overview

- **Total Problems Solved**: {total}
- **Average Problem Rating**: {avg_rating}
- **Active Rating Ranges**: {solved_ratings}/{total_possible_ratings}

{cf_section}

{detailed_table}

*Updated automatically*
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    if not os.path.exists('problems'):
        os.makedirs('problems')
    
    # Get Codeforces rating
    cf_rating, cf_max_rating, cf_rank = get_codeforces_rating('thehandsomeone')
    
    progress, total, avg_rating = count_solutions()
    update_readme(progress, total, avg_rating, cf_rating, cf_max_rating, cf_rank)

if __name__ == "__main__":
    main()