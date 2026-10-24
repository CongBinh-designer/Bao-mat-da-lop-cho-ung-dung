# Kịch bản kiểm thử bảo mật WAF tự động - Tuần 3
$ALB_DNS = "http://Lab-ALB-Public-1339636236.us-east-1.elb.amazonaws.com"

Write-Host "=== TEST CASE 1: SQL Injection ===" -ForegroundColor Yellow
curl.exe -i "$ALB_DNS/?id=1%20OR%201=1"

Write-Host "`n=== TEST CASE 2: Cross-Site Scripting (XSS) ===" -ForegroundColor Yellow
curl.exe -i "$ALB_DNS/?q=<script>alert(1)</script>"

Write-Host "`n=== TEST CASE 3: HTTP Flood / Rate Limiting (130 Requests) ===" -ForegroundColor Yellow
1..130 | ForEach-Object {
    $code = curl.exe -s -o NUL -w "%{http_code}" "$ALB_DNS/"
    Write-Host "Request #$_ - Status: $code"
}
