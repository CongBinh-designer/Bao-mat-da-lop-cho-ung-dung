# Ứng dụng Bảo mật Đa lớp trên AWS

## Thông tin sinh viên & Đồ án
* **Môn học:** Điện toán đám mây (Cloud Computing) - Đợt 1
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Nhóm thực hiện:**
  * Nguyễn Xuân Nhật - MSSV: 24110293
  * Nguyễn Công Bình - MSSV: 24110168
* **AWS Region:** `us-east-1` (N. Virginia)

## Cấu trúc phòng thủ đa lớp (5 Layers)
1. **Lớp 1 (Edge Protection):** AWS WAF gắn trên Application Load Balancer.
2. **Lớp 2 (Network & Isolation):** Subnet phân tầng (Public/Private), NACL và Security Groups 3-tier.
3. **Lớp 3 (Credential Management):** AWS Secrets Manager lưu trữ thông tin đăng nhập database.
4. **Lớp 4 (Data Encryption):** AWS KMS mã hóa dữ liệu tĩnh (EBS, RDS, S3).
5. **Lớp 5 (Threat Detection):** Amazon GuardDuty giám sát liên tục VPC Flow Logs & DNS logs.

## Tiến độ thực hiện
- [x] **Tuần 1:** Thiết kế kiến trúc 3 tầng, mô hình STRIDE, khởi tạo VPC, 6 Subnets, S3 Bucket, Security Groups.
- [x] **Tuần 2:** Khởi tạo RDS MySQL, AWS Secrets Manager, EC2 Web App (`LabInstanceProfile`), Application Load Balancer và kiểm thử an ninh cách ly mạng.
- [x] **Tuần 3:** Cấu hình AWS WAF trên ALB, kích hoạt Amazon GuardDuty và thiết lập giám sát CloudWatch.
- [ ] **Tuần 4:** Tối ưu hóa chi phí, tổng kết báo cáo, quay video demo hoàn chỉnh.
