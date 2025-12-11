cd ../..
rm -rf dist
poetry build
export TWINE_HTTP_TIMEOUT=60
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
