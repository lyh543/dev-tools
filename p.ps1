Push-Location ~\git\blog

Write-Output "`npushing to lyh543/blog`n"

git add --all
git commit -m "blog: update on $(Get-Date)"
git push origin master

Pop-Location