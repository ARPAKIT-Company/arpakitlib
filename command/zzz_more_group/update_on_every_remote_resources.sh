cd ../..

git add .
git commit -m "fix"
git push primary
git push mirror_1

export TWINE_HTTP_TIMEOUT=60

rm -rf dist
poetry build
poetry publish --repository testpypi
poetry publish
