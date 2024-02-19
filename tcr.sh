git add .
pytest test && git commit -m "$1" || git reset --hard