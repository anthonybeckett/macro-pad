$currDir = Get-Location
$driveLabel = "CIRCUITPY"

if($null -ne (Get-Volume -FileSystemLabel $driveLabel)){
    $targetDrive = (Get-Volume -FileSystemLabel $driveLabel).DriveLetter
    $filePath = $targetDrive + ":\code.py"

    if ((Test-Path -Path $filePath -PathType Leaf)) {
        Remove-Item $filePath
    }

    Write-Output $targetDrive

    Copy-Item ${currDir}\*.py ${targetDrive}:\

    Write-Output "Success!"

    exit 0
} else {
    Write-Output "Pico not found"
    exit 1
}
