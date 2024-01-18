# test
$root_path = (Get-Item "$PSScriptRoot/..").FullName
$src_path = "$root_path/src"
pip install -U pytest pytest-cov --quiet
$Env:PYTHONPATH=$src_path
Write-Host "Python path:" $Env:PYTHONPATH
pytest "$root_path/tests"  --exitfirst --log-level=INFO --cov $Env:PYTHONPATH --cov-report=xml