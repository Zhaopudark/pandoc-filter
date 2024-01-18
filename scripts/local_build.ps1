# This script file is for local machine only, without considering any configuration or installation.
$ErrorActionPreference = 'Stop'
$root_path = (Get-Item "$PSScriptRoot/..").FullName
$src_path = "${root_path}/src"
$release_note_path = "${root_path}/RELEASE.md"
python "${PSScriptRoot}/check_release_version.py" $src_path $release_note_path
if ($LastExitCode -ne 0) {
    throw "The release version in ${PSScriptRoot}/check_release_version.py is not consistent with the given version in ${root_path}/src/pandoc_filter/__init__.py."
}
python -m build