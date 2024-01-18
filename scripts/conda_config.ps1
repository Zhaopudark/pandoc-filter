$ErrorActionPreference = 'Stop'

if (Get-Command conda -ErrorAction SilentlyContinue) {
    Write-Host "Conda detected, use conda."
    $conda_env_name = "pandoc_filter_dev"
    if (-not (conda env list | Select-String -Pattern $conda_env_name)) {
        conda create --name $conda_env_name python=3.12 --yes --quiet
    } 
    conda activate $conda_env_name
    conda install --update-deps pandoc>=3.1 -c conda-forge --yes --quiet
} else {
    Write-Host "Conda not detected."
    if (Get-Command pandoc -ErrorAction SilentlyContinue) {
        Write-Host "Pandoc detected."
    }else{
        Write-Host "Pandoc not detected, install pandoc."
        if($IsLinux){
            wget https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-1-amd64.deb -o pandoc-amd64.deb
            sudo dpkg -i pandoc-amd64.deb
        }elseif($IsWindows){
            winget search pandoc
            winget install --id JohnMacFarlane.Pandoc
        }else{
            throw "Unsupported platform. Only Linux and Windows are supported."
        }
    }
}