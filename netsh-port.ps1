switch ($args[0]) {
    "list" { netsh interface ipv4 show excludedportrange protocol=tcp }
    "add" { netsh interface ipv4 add excludedportrange protocol=tcp numberofports=100 startport=$args[1] }
    "del" { netsh interface ipv4 delete excludedportrange protocol=tcp numberofports=100 startport=$args[1] }
    Default {
        Write-Output "Usage: $0 [list|add <startport>|del <startport>]"
    }
}