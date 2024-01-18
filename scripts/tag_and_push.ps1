$version = . "${PSScriptRoot}/check_release_version.ps1"
# Write-Host 

$tagName = "v${version}"
# 检测标签是否存在
if (git show-ref --quiet "refs/tags/$tagName") {
    # 标签存在，删除它
    git tag -d $tagName
    Write-Output "Tag '$tagName' deleted."
} else {
    # 标签不存在
    Write-Output "Tag '$tagName' does not exist."
    Write-Output "Creating tag '$tagName'."
}
git tag -a $tagName -m "Release $tagName"

# 检测远程标签是否存在
$remoteTagExists = git ls-remote --tags origin | Where-Object { $_ -match "refs/tags/$tagName" }

if ($remoteTagExists) {
    # 远程标签存在，删除它
    git push origin --delete $tagName
    Write-Output "Remote tag '$tagName' deleted."
} else {
    # 远程标签不存在
    Write-Output "Remote tag '$tagName' does not exist."
    Write-Output "Pushing tag '$tagName' to remote."
}
git push origin $tagName