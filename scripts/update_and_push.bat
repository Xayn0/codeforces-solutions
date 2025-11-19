@echo off
python update_progress.py
git add .
git commit -m "Add new solutions"
git push origin main