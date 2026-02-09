$response = Invoke-RestMethod -Uri "http://localhost:8000/generate_image" -Method Post -Body (@{prompt="A futuristic cyberpunk city"} | ConvertTo-Json) -ContentType "application/json"
if ($response.image_base64.Length -gt 100) { Write-Host "Success: Image Generated" } else { Write-Error "Failed" }
