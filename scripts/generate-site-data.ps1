$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$repoUrl = ""
$repoBirthDate = ""
$addedDates = @{}
$supportedExtensions = @('.py', '.cpp', '.cc', '.cxx', '.c', '.java', '.js', '.ts', '.cs', '.go', '.rb', '.php', '.swift', '.kt', '.rs')

try {
  $repoUrl = (git -C $repoRoot remote get-url origin 2>$null).Trim() -replace '\.git$', ''
} catch {
  $repoUrl = ""
}

try {
  $commitDates = @(git -C $repoRoot log --format=%aI 2>$null)
  if ($commitDates.Count -gt 0) {
    $repoBirthDate = $commitDates[-1].Substring(0, 10)
  }
} catch {
  $repoBirthDate = ""
}

Get-ChildItem -Path $repoRoot -File | ForEach-Object {
  $name = $_.Name
  $extension = $_.Extension.ToLowerInvariant()

  if ($supportedExtensions -notcontains $extension) {
    return
  }

  if ($name -notmatch '^\d+\.\s*.+') {
    return
  }

  try {
    $createdAt = (git -C $repoRoot log --diff-filter=A --format=%aI -- "$name" 2>$null | Select-Object -First 1)
    if (-not [string]::IsNullOrWhiteSpace($createdAt)) {
      $addedDates[$name] = $createdAt.Trim()
    }
  } catch {
  }
}

$metadata = @{
  repoUrl = $repoUrl
  repoBirthDate = $repoBirthDate
  addedDates = $addedDates
}

$tempPath = [System.IO.Path]::GetTempFileName()
Set-Content -Path $tempPath -Value ($metadata | ConvertTo-Json -Depth 10) -Encoding UTF8
$env:SITE_GIT_METADATA_PATH = $tempPath
node (Join-Path $repoRoot "scripts/generate-site-data.js")
Remove-Item $tempPath -ErrorAction SilentlyContinue
