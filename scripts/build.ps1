$ErrorActionPreference = 'Stop'
if (Get-Command conda -ErrorAction SilentlyContinue) {
    Write-Host "Conda detected, use conda."
    $conda_env_name = "pandoc_filter_dev"
    if (-not (conda env list | Select-String -Pattern $conda_env_name)) {
        conda create --name $conda_env_name python=3.12 --yes
    } 
    conda activate $conda_env_name
} else {
    Write-Host "Conda not detected, use pip."
}
pip install -r "${PSScriptRoot}/requirements.txt"
pip install -U setuptools build
python -m build



