cd ..

git add .
git commit -m "fix"
git push arpakit_company_github_1 dev
git push arpakit_company_gitlab_1 dev

export TWINE_HTTP_TIMEOUT=60

rm -rf dist
poetry build
poetry publish --repository testpypi
poetry publish
