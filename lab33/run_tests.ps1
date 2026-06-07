Set-StrictMode -Version Latest
Push-Location -Path $PSScriptRoot
try {
    Write-Host "Installing requirements..."
    python -m pip install -r requirements.txt
    Write-Host "Running pytest..."
    & "C:/Users/Lenovo Yoga/AppData/Local/Programs/Python/Python314/python.exe" -m pytest -q
} finally {
    Pop-Location
}
