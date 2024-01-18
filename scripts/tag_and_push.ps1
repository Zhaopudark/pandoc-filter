$version = . "${PSScriptRoot}/check_release_version.ps1"
$tagName = "v${version}"

# 检测标签是否存在
if (git show-ref "refs/tags/$tagName") {
    # 标签存在，强制覆盖
    Write-Output "Covering tag '$tagName' forcibly."
    git tag -a $tagName -m "Release $tagName" --force
} else {
    # 标签不存在
    Write-Output "Tag '$tagName' does not exist."
    Write-Output "Creating tag '$tagName'."
    git tag -a $tagName -m "Release $tagName"
}

# 检测远程标签是否存在
if (git ls-remote --tags origin | Where-Object { $_ -match "refs/tags/$tagName" }) {
    # 远程标签不存在
    Write-Output "Covering remote tag '$tagName' forcibly."
    git push origin $tagName --force
} else {
    # 远程标签不存在
    Write-Output "Remote tag '$tagName' does not exist."
    Write-Output "Pushing tag '$tagName' to remote."
    git push origin $tagName
}
