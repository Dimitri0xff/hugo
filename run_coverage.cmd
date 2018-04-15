coverage run --source=bot -m unittest discover
coverage report
@coverage html -d out/coverage_html
