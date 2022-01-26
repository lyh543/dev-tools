foreach ($file in $args) {
    Remove-Item $file -Force -Confirm:$false -Recurse &&
        Write-Output "Successfully remove $file"
}