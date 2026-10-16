## TUẦN 1: TÌM HIỂU DỊCH VỤ, THIẾT KẾ KIẾN TRÚC & DỰNG NỀN TẢNG HẠ TẦNG

* **Thời gian thực hiện:** 05/10/2026 – 11/10/2026
* **Mục tiêu tuần 1:**
  1. Nghiên cứu tài liệu các dịch vụ bảo mật: AWS WAF, VPC, EC2, ELB, RDS, KMS, Secrets Manager, GuardDuty.
  2. Thiết kế mô hình kiến trúc phòng thủ đa lớp (Defense-in-Depth) và vẽ sơ đồ hệ thống trên draw.io.
  3. Khởi tạo hạ tầng mạng cơ bản: VPC (`10.0.0.0/16`), 6 Subnets (2 Public, 2 Private App, 2 Private DB), Internet Gateway, Route Tables, S3 Gateway Endpoint.
  4. Khởi tạo S3 bucket lưu trữ logs, kích hoạt mã hóa tại chỗ (SSE-S3), chặn truy cập công khai (Block Public Access) và gắn Tag.
  5. Cấu hình 3 Security Groups nền tảng (`SG-ALB`, `SG-EC2`, `SG-RDS`) theo nguyên tắc đặc quyền tối thiểu (Least Privilege).
  6. Khảo sát chính sách phân quyền `LabRole` / `LabInstanceProfile`.
  7. Xây dựng bản dự thảo Mô hình đe dọa (Threat Modeling) theo chuẩn STRIDE.

---

### 1. BẢNG TỔNG HỢP PHÂN CÔNG VÀ GIỜ LÀM VIỆC TUẦN 1

| Sinh viên | MSSV | Vai trò chính |
| :--- | :---: | :--- |
| **Nguyễn Xuân Nhật** | 24110293 | Thiết kế kiến trúc, Dựng nền tảng VPC, Subnets, S3 Bucket |
| **Nguyễn Công Bình** | 24110168 | Soạn thảo STRIDE, Khảo sát LabRole, Mở rộng DB Subnets, Cấu hình 3 Security Groups |

---

### 2. CHI TIẾT CÔNG VIỆC TỪNG SINH VIÊN

#### Sinh viên 1: Nguyễn Xuân Nhật (MSSV: 24110293)
• Phác thảo và vẽ sơ đồ kiến trúc tổng thể bằng draw.io.

• Tạo VPC `Lab-VPC` (CIDR `10.0.0.0/16`) trên AWS Management Console, 2 Public Subnets và 2 Private App Subnets trên 2 AZ (`us-east-1a`, `us-east-1b`).

• Cấu hình Internet Gateway (`Lab-VPC-igw`), Route Tables và S3 Gateway Endpoint (`Lab-VPC-vpce-s3`).

• Khởi tạo S3 Bucket `sec-app-logs-24110293-24110168-us-east-1`. Bật tính năng Block All Public Access và mã hóa mặc định SSE-S3.

• Gắn nhãn Tagging (`Project`, `Owner`, `Environment`) cho VPC và S3 bucket.

---

#### Sinh viên 2: Nguyễn Công Bình (MSSV: 24110168)

• Nghiên cứu và soạn thảo bản dự thảo tài liệu Threat Modeling phân tích chi tiết 6 khía cạnh: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.

• Khảo sát danh sách quyền của `LabRole` và `LabInstanceProfile` trên IAM Console.


• Cấu hình 3 Security Groups liên kết chặt chẽ.

• Thiết lập Git repository chung cho nhóm trên GitHub.

---
## TUẦN 2: TRIỂN KHAI CÁC CHỨC NĂNG LÕI TRÊN AWS & KIỂM THỬ THÀNH PHẦN

- **Thời gian thực hiện:** 12/10/2026 – 18/10/2026
- **Mục tiêu tuần 2:**
  1. Khởi tạo DB Subnet Group và triển khai cụm cơ sở dữ liệu Amazon RDS MySQL trong dải mạng nội bộ (Private DB Subnets).
  2. Kích hoạt tính năng mã hóa dữ liệu tĩnh (At-Rest Encryption) trên RDS sử dụng AWS KMS.
  3. Lưu trữ và quản lý thông tin xác thực cơ sở dữ liệu trên AWS Secrets Manager theo chuẩn Zero Hardcoded Secrets.
  4. Khởi chạy máy ảo EC2 Web Server, gắn `LabInstanceProfile` (`LabRole`) để phân quyền tự động qua STS Token.
  5. Thiết lập nhóm bảo mật `Lab-EC2-SG` áp dụng nguyên tắc đặc quyền tối thiểu (Least Privilege), chỉ nhận lưu lượng từ ALB.
  6. Triển khai Application Load Balancer (`Lab-ALB-Public`) đa vùng sẵn sàng (Multi-AZ) và ánh xạ Target Group (`TG-EC2-App`).
  7. Lập trình kịch bản nạp Secret động, thực hiện kiểm thử tích hợp (Integration Testing) và kiểm thử cách ly an ninh (Security Isolation Testing).

---

### 1. BẢNG TỔNG HỢP PHÂN CÔNG VÀ GIỜ LÀM VIỆC TUẦN 2

| Sinh viên | MSSV | Vai trò chính |
| :--- | :---: | :--- |
| **Nguyễn Xuân Nhật** | 24110293 | Cấu hình DB Subnet Group, Khởi tạo RDS MySQL, Cấu hình ALB & Target Group, Kiểm thử định tuyến và cách ly DB |
| **Nguyễn Công Bình** | 24110168 | Cấu hình Secrets Manager, Dựng máy ảo EC2 & gán IAM Role, Lập trình ứng dụng nạp secret động, Kiểm thử cách ly máy chủ |

---

### 2. CHI TIẾT CÔNG VIỆC TỪNG SINH VIÊN

#### Sinh viên 1: Nguyễn Xuân Nhật (MSSV: 24110293)
- Tạo DB Subnet Group `lab-rds-subnet-group` liên kết 2 Subnet nội bộ trên 2 Availability Zones (`us-east-1a`, `us-east-1b`).

- Khởi tạo cơ sở dữ liệu Amazon RDS MySQL `sec-app-db` (Instance class `db.t4g.micro`), cấu hình `Publicly accessible = No` và gán nhóm bảo mật `Lab-RDS-SG`.

- Xác thực cấu hình mã hóa lưu trữ tầng phần cứng (Storage Encryption Enabled) trên RDS MySQL bằng khóa dịch vụ AWS KMS (`aws/rds`).

- Cấu hình Application Load Balancer `Lab-ALB-Public` thuộc `Lab-VPC` trải trên 2 Public Subnet, gán nhóm bảo mật `Lab-ALB-SG`.

- Tạo Target Group `TG-EC2-App` (giao thức HTTP, port 80), đăng ký máy ảo EC2 làm target và xác nhận trạng thái Healthy qua Health Check.

- Thực hiện kiểm thử tích hợp truy cập ứng dụng web thành công từ Internet qua địa chỉ DNS công khai của ALB.

- Thực hiện kiểm thử cách ly cơ sở dữ liệu bằng lệnh `curl` từ môi trường ngoài tới cổng 3306 của RDS Endpoint, xác nhận kết nối thất bại (Timed out).

---

#### Sinh viên 2: Nguyễn Công Bình (MSSV: 24110168)

- Khởi tạo Secret `production/sec-app/rds-credentials` trên AWS Secrets Manager lưu trữ an toàn thông tin tài khoản `adminapp` và mật khẩu truy cập RDS.

- Mã hóa bí mật trên Secrets Manager bằng khóa AWS KMS và gắn nhãn Tagging chuẩn hóa (`Project`, `Owner`, `Environment`).

- Khởi chạy máy ảo `Lab-EC2-WebServer` (`t2.micro`) thuộc `Lab-VPC`, gán `LabRole` thông qua `LabInstanceProfile` để cấp quyền truy xuất AWS SDK.

- Thiết lập cấu hình Inbound Rules cho Security Group `Lab-EC2-SG`, chỉ cho phép traffic cổng 80/5000 có nguồn bắt nguồn đích danh từ `Lab-ALB-SG`.

- Viết mã nguồn Python (`test_secret_rds.py`) sử dụng thư viện `boto3` và `pymysql` để giải mã secret động lúc runtime và kết nối tới RDS MySQL theo chuẩn Zero Hardcoded Secrets.

- Thực thi kịch bản kiểm thử trực tiếp trên máy chủ EC2, xác thực việc đọc Secret và mở luồng TCP thành công tới cổng 3306 của RDS.

- Thực hiện kiểm thử cách ly máy chủ Web EC2 bằng cách truy cập trực tiếp qua Public IP từ trình duyệt bên ngoài, xác nhận kết nối bị chặn hoàn toàn (`ERR_CONNECTION_TIMED_OUT`).
