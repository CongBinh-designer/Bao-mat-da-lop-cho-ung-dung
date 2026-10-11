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
