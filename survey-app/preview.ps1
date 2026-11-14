param([ValidateSet("start","stop","status")][string]$Action="status",[int]$Port=5187)
$ErrorActionPreference="Stop"
$project=(Get-Item -LiteralPath $PSScriptRoot).Parent.FullName
$runtimeDir=Join-Path $project "local-data/direct-hop-survey/simulation"
$pidFile=Join-Path $runtimeDir "preview-$Port.pid"
$processId=0
if(Test-Path -LiteralPath $pidFile){
    $processId=[int](Get-Content -LiteralPath $pidFile -Raw)
}
$owned=if($processId){Get-Process -Id $processId -ErrorAction SilentlyContinue}
if($Action -eq "status"){
    if($owned){Write-Output "Preview PID $processId on loopback port $Port"}else{Write-Output "Stopped"}
    return
}
if($Action -eq "stop"){
    if($owned){
        $marker=Join-Path $runtimeDir "stop-$processId"
        [IO.File]::WriteAllText($marker,"stop")
        if(-not $owned.WaitForExit(12000)){throw "Stop marker not acknowledged; verify the recorded PID."}
    }
    if(Test-Path -LiteralPath $pidFile){Remove-Item -LiteralPath $pidFile}
    return
}
if($owned){throw "Recorded preview PID $processId is active"}
New-Item -ItemType Directory -Force -Path $runtimeDir | Out-Null
$python=(Get-Command python -CommandType Application | Select-Object -First 1).Source
$proc=Start-Process -FilePath $python -ArgumentList @("survey-app/server.py","--source","simulation","--port",$Port) -WorkingDirectory $project -WindowStyle Hidden -PassThru -RedirectStandardOutput (Join-Path $runtimeDir "host.out") -RedirectStandardError (Join-Path $runtimeDir "host.err")
Start-Sleep -Milliseconds 650
if($proc.HasExited){throw (Get-Content -LiteralPath (Join-Path $runtimeDir "host.err") -Raw)}
[IO.File]::WriteAllText($pidFile,[string]$proc.Id)
Write-Output "Started private simulation PID $($proc.Id) on 127.0.0.1:$Port"
