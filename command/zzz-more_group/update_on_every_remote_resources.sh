cd ../..

git add .
git commit -m "fix"
git push git_main_repository_address
git push git_another_repository_address_1

export TWINE_HTTP_TIMEOUT=60

rm -rf dist
poetry build
poetry publish --repository testpypi
poetry publish
