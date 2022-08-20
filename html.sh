echo "Generating Coverage HTML Report"
pipenv run coverage html
echo "Starting Browser"
start "htmlcov/index.html"