@echo off
python scripts\update_progress.py
git add .
git commit -m "Add new solutions - auto update"
git push origin main
pause