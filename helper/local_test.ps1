conda activate pandoc
pip install -U pytest pytest-cov
$root_path = (Get-Item "$PSScriptRoot/..").FullName
$Env:PYTHONPATH="$root_path/src"
Write-Host "Python path:" $Env:PYTHONPATH
pytest .\tests\  --log-level=INFO --cov $Env:PYTHONPATH --cov-report=xml