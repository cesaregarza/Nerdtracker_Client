echo "Running dev.sh, a group of commands for linting and testing."
echo "Running isort."
pipenv run isort .
echo "Running black."
pipenv run black .
echo "Running flake8."
pipenv run flake8 .
echo "Running mypy."
pipenv run mypy .
echo "Running pytest."
pipenv run pytest . -vv