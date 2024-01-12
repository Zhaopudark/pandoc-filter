conda activate pandoc
pip install pytest pytest-cov
# get-item "${PSScriptRoot}/dist/*.whl"
pip install (Get-Item "${PSScriptRoot}/../dist/*.whl").FullName --force
# https://docs.codecov.com/docs/code-coverage-with-python
$package_location = (pip show pip | Select-String -Pattern 'Location: (.+)' | ForEach-Object { $_.Matches.Groups[1].Value }).Trim()
pytest ./tests --cov "${package_location}/pandoc_filter"