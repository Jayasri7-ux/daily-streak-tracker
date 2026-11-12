# Register-DailyStreakTask.ps1
# Optional: Registers a daily background task in Windows Task Scheduler
# so `auto_streak.py` also runs locally on your PC every day at 7:00 PM.

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonPath = (Get-Command python).Source
$PythonScript = Join-Path $ScriptDir "auto_streak.py"

$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$PythonScript`"" -WorkingDirectory $ScriptDir
$Trigger = New-ScheduledTaskTrigger -Daily -At 7:00PM
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "GitHubDailyStreakBot" -Action $Action -Trigger $Trigger -Settings $Settings -Description "Automatically commits and pushes daily activity to GitHub" -Force
Write-Host "Successfully registered 'GitHubDailyStreakBot' in Windows Task Scheduler (Daily at 7:00 PM)!" -ForegroundColor Green
