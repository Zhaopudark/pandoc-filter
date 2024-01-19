# This script file is for local machine only, without considering any configuration or installation.
$ErrorActionPreference = 'Stop'
$root_path = (Get-Item "$PSScriptRoot/..").FullName
$src_path = "${root_path}/src"
$release_note_path = "${root_path}/RELEASE.md"
$version = python "${PSScriptRoot}/check_release_version.py" $src_path $release_note_path
# Write-Host $version
if ($LastExitCode -ne 0) {
    throw "The release version in ${release_note_path} is not consistent with the given version in ${root_path}/src/pandoc_filter/__init__.py."
}
return $version