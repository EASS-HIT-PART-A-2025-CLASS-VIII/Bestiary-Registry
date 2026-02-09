$headers = @{ "Content-Type" = "application/json" }
$body = @{
    name = "AsyncDragon_$(Get-Random)"
    mythology = "Norse"
    creature_type = "Dragon"
    danger_level = 10
    habitat = "Volcano"
} | ConvertTo-Json

# 1. Create Creature
Write-Host "Creating creature..."
$response = Invoke-RestMethod -Uri "http://localhost:8000/creatures/" -Method Post -Body $body -Headers $headers
$id = $response.id
Write-Host "Creature created with ID: $id"

# 2. Poll for Image Status
for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Seconds 2
    $c = Invoke-RestMethod -Uri "http://localhost:8000/creatures/$id"
    Write-Host "Status: $($c.image_status) - URL: $($c.image_url)"
    
    if ($c.image_status -eq "ready") {
        Write-Host "SUCCESS: Image is ready!"
        # Verify URL availability
        try {
            $img = Invoke-WebRequest -Uri "http://localhost:8000$($c.image_url)" -Method Head
            if ($img.StatusCode -eq 200) {
                Write-Host "SUCCESS: Image file is accessible."
                exit 0
            }
        } catch {
            Write-Error "Failed to access image URL."
        }
        break
    }
    if ($c.image_status -eq "failed") {
        Write-Error "Job failed: $($c.image_error)"
        exit 1
    }
}
exit 0
