Param(
    [String]$FfmpegPath,
    [String]$FolderPath,
    [String]$DestinationFolderPath,
    [String]$File
)

function Convert-All {

    $ffmpeg = $FfmpegPath

    if ($FolderPath) {
        Set-Location -Path $FolderPath
        
    } 

    $allmp4files = Get-Item *.mp4

    if ($DestinationFolderPath) {
        foreach($file in $allmp4files) {
            Write-Host $ffmpeg
            & "$($ffmpeg)" -y -i $file -vn -acodec libmp3lame -ar 44100 -ab 128k -f mp3 "$DestinationFolderPath\$($file.BaseName).mp3"
        }
    } else {
        foreach($file in $allmp4files) {
            & "$ffmpeg" -y -i $file -vn -acodec libmp3lame -ar 44100 -ab 128k -f mp3 "$file.mp3"
        }
    }
    
}

function Convert-File {
    # The route of the file must be a complete path
    $current_file = Get-Item -Path "$File"
    & "$($FfmpegPath)" -y -i $current_file -vn -acodec libmp3lame -ar 44100 -ab 128k -f mp3 "$DestinationFolderPath\$($current_file.BaseName).mp3"
}




if ($File) {
    Convert-File
} else {
    Convert-All
    
}