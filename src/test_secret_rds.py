import json
import boto3
import pymysql

region_name = "us-east-1"
secret_name = "production/sec-app/rds-credentials"

print("[*] Đang kết nối tới AWS Secrets Manager...")
client = boto3.client(service_name="secretsmanager", region_name=region_name)

try:
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])
    print("[+] Đọc Secret thành công mà KHÔNG cần hardcode key!")
    print(f"  - Username: {secret.get('username')}")
    print(f"  - Engine: {secret.get('engine')}")
    print(f"  - Host: {secret.get('host')}")

    print("\n[*] Đang thử kết nối vào cơ sở dữ liệu RDS MySQL...")
    conn = pymysql.connect(
        host=secret.get("host"),
        user=secret.get("username"),
        password=secret.get("password"),
        connect_timeout=5
    )
    print("[+] KẾT NỐI RDS MYSQL THÀNH CÔNG!")
    conn.close()

except Exception as e:
    print("[-] Lỗi phát sinh:", str(e))
