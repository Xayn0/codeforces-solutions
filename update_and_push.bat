@echo off
echo Updating README and pushing to GitHub...
python scripts\update_progress.py
git add .
git commit -m "Add new solutions - auto update"
git push origin main
echo Done!
pause