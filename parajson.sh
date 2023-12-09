$headers = @{
    "Content-Type" = "application/json"
}

$data = ' {"id": 1, "nombre": "Juan Pérez"}'

Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/data" -Method Post -Headers $headers -Body $data
