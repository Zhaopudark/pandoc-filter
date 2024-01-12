# $latestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/jgm/pandoc/releases/latest"
# $latestVersion = $latestRelease.tag_name
# Write-Host "Latest version: $latestVersion"
wget https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-1-amd64.deb
sudo dpkg -i pandoc-3.1.11-1-amd64.deb
pip install -r "${PSScriptRoot}/requirements.txt"
pip install -U setuptools build
python -m build