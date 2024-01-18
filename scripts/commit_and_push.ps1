param (
    [Parameter(Mandatory)]
    [string]$message
)
# 获取当前所在的分支
$currentBranch = git rev-parse --abbrev-ref HEAD

if ($currentBranch -eq "main") {
    # 如果当前分支是 dev 分支，则进行 commit 操作
    . "${PSScriptRoot}/check_release_version.ps1"
    git add .  # 添加需要提交的文件（假设你要提交所有文件）
    git commit -m $message
    git push
} else {
    Write-Host "Not on main branch. Current branch: $currentBranch"
}