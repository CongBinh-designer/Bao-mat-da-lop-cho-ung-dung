Spoofing (Giả mạo danh tính)	ALB (Public Entry)

EC2 Web App
	Kẻ tấn công giả mạo địa chỉ IP, giả mạo Client hoặc giả lập các HTTP request hợp lệ để truy cập tài nguyên nội bộ trái phép.	AWS WAF: Lọc header giả mạo, kiểm tra IP Reputation List.

NACL & Security Group: Chỉ cho phép traffic đi qua ALB hợp lệ; EC2 chỉ nhận traffic từ ALB.

Tampering (Can thiệp / Sửa đổi dữ liệu)	Dữ liệu truyền tải (In-transit)


Dữ liệu lưu trữ (At-rest: EBS, RDS, S3)
	Man-in-the-Middle (MitM) nghe lén hoặc sửa đổi gói tin HTTP.

Kẻ xấu/mã độc sửa đổi trái phép dữ liệu trong DB hoặc file log trên S3.	HTTPS / TLS: Mã hóa đường truyền từ Client đến ALB.

AWS KMS: Mã hóa toàn bộ volume EBS, database RDS và S3 Bucket (SSE-KMS/SSE-S3).

S3 Versioning / Object Lock: Chống xóa, chống sửa đổi log.
Repudiation (Chối bỏ trách nhiệm)	Toàn bộ hệ thống (ALB,EC2,Database)	Kẻ tấn công hoặc người dùng nội bộ thực hiện hành vi phá hoại/truy vấn độc hại nhưng không lưu lại vết để điều tra và quy trách nhiệm.	Amazon GuardDuty: Giám sát liên tục VPC Flow Logs và DNS query logs để phát hiện hành vi bất thường.

ALB Access Logs & S3: Bật logging toàn bộ request chuyển tiếp về S3.

CloudWatch Logs: Ghi log hoạt động của ứng dụng.
Information Disclosure (Lộ lọt thông tin)	EC2 Web Server

Mã nguồn & File cấu hình

Cơ sở dữ liệu RDS	Lộ username/password database trong mã nguồn GitHub hoặc file cấu hình trên EC2.

Lộ lọt dữ liệu người dùng qua lỗ hổng SQL Injection.

Database bị quét cổng trực tiếp từ Internet.	AWS Secrets Manager: Lưu trữ credentials tập trung, nạp động vào RAM khi ứng dụng khởi chạy.
AWS WAF: Bật bộ quy tắc AWSManagedRulesSQLiRuleSet chặn triệt để SQL Injection.
Private Subnets: Đặt RDS và EC2 hoàn toàn trong mạng Private, ngắt Public IP.
Denial of Service (Từ chối dịch vụ - DoS/DDoS)	ALB

EC2 Compute Instance	Kẻ tấn công gửi hàng triệu request liên tục (HTTP Flood) làm cạn kiệt tài nguyên CPU/RAM của EC2 hoặc làm sập đường truyền mạng.	AWS WAF Rate-based Rule: Tự động chặn tạm thời bất kỳ IP nào gửi vượt quá ngưỡng (ví dụ: > 100 requests / 5 phút).

AWS Shield Standard: Mặc định bảo vệ chống DDoS tầng L3/L4 cho ALB.

ALB Distribution: Phân phối tải đều qua các AZs.

Elevation of Privilege (Leo thang đặc quyền)
	Máy chủ EC2

Quyền IAM trên AWS	Kẻ tấn công chiếm được shell trên EC2, sau đó tìm cách chiếm quyền Root hệ điều hành hoặc lấy cắp AWS Token để thao túng các tài nguyên đám mây khác.	IAM LabRole / LabInstanceProfile: Chỉ gán quyền tối thiểu cần thiết cho EC2 (Principle of Least Privilege).

Security Group EC2: Chặn mở SSH (port 22) ra ngoài Internet, chỉ quản lý qua EC2 Instance Connect / SSM nếu cần.

Security Group RDS: Chỉ chấp nhận duy nhất Inbound kết nối từ SG-EC2.
