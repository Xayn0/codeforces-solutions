@echo off
echo Starting update...
python scripts\update_progress.py
git add .
git commit -m "Update solutions and stats"
git push origin main
echo Update complete!
pause