# Báo cáo Tuần 4

## I. Worklog
**Thời gian thực hiện: 26/10/2026 – 1/11/2026**

**Nguyễn Xuân Nhật (MSSV: 24110293) Thời gian: 8h**
- Viết kịch bản kiểm thử cho toàn bộ dự án (2 giờ)
- Tối ưu hóa chi phí và dọn dẹp tài nguyên tránh phát sinh chi phí ngầm (3 giờ)
- Viết báo cáo về dự án (3 giờ)

**Nguyễn Công Bình (MSSV: 24110168) Thời gian: 8h**
- Quay và chỉnh sửa video demo toàn bộ dự án theo kịch bản (4 giờ)
- Chuẩn hóa mã nguồn, hợp nhất các file CloudFormation (2 giờ)
- Cập nhật toàn bộ GitHub của nhóm và tổng kết WORKLOG 4 tuần (2 giờ)

---

## II. Sơ đồ kiến trúc dự án

<img width="940" height="496" alt="image" src="https://github.com/user-attachments/assets/a3b7b27a-ee3d-4b98-a68b-6693ab9a2b9e" />


*Hình 1.1: Sơ đồ kiến trúc tổng thể*

- Đây là sơ đồ kiến trúc nhóm em đã lên kế hoạch cho dự án từ tuần đầu tiên.
- Dự án được bảo mật qua 5 lớp phòng thủ dựa theo mô hình đe dọa STRIDE được phát triển bởi Microsoft: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege.

---

## III. Kiểm thử tổng thể dự án

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/f066e144-cbac-4e33-a654-53b75034a12c" />


*Hình 2.1: Ứng dụng web truy xuất thành công cơ sở dữ liệu RDS*

**Nhận xét:**
- Khi người dùng thực hiện kết nối tới trang web thông qua đường link http://Lab-ALB-Public-1339636236.us-east-1.elb.amazonaws.com sẽ truy cập vào trang web thành công.
- Nhờ cơ chế của IAM Role và Secrets Manager giúp ứng dụng kết nối tới RDS MySQL an toàn tuyệt đối mà không cần lưu trữ mật khẩu tĩnh trong mã nguồn.

<img width="940" height="794" alt="image" src="https://github.com/user-attachments/assets/dbc0e9a9-65a4-46aa-a9c4-0f6a42b49213" />


*Hình 2.2: Security Group chặn truy cập trực tiếp vào máy chủ EC2 qua IP.*

**Nhận xét:**
Khi gõ thử public IP của EC2 lên trình duyệt thì trang web sẽ bị treo và báo lỗi kết nối chứng minh rằng Security Group đã khóa chặt, kẻ gian không thể đi đường tắt.

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/fc07df3c-a369-496d-9902-6309cd807c5b" />


*Hình 2.3: Phản hồi HTTP 403 Forbidden khi kẻ gian tấn công SQL Injection*

**Nhận xét:**
Sau khi thêm vào `?id=1%20OR%201=1` phía sau đuôi của đường link nhằm đánh cắp thông tin bằng SQL Injection. Bộ lọc WAF SQLiRuleSet đã phát hiện và chặn đứng yêu cầu ngay lập tức.

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/775b3d78-d729-4ab5-9535-65e953a288f4" />


*Hình 2.4: Phản hồi HTTP 403 Forbidden ngăn chặn tấn công Cross-Site Scripting (XSS)*

**Nhận xét:**
Khi dán đường dẫn có đoạn mã JavaScript http://lab-alb-public-1339636236.us-east-1.elb.amazonaws.com/?q=<script>alert(1)</script> liền bị WAF chặn lại.

<img width="940" height="483" alt="image" src="https://github.com/user-attachments/assets/219fe1ac-1f95-42d5-ae81-4dc927f00e95" />


*Hình 2.5: Gửi dồn dập 130 requests làm cạn kiệt tài nguyên*

**Nhận xét:**
Sau khi chạy lệnh trên PowerShell nhằm gửi dồn dập 130 requests hệ thống tự động khóa IP và trả về mã lỗi 403 nhờ quy tắc RateLimit-100.

<img width="940" height="494" alt="image" src="https://github.com/user-attachments/assets/830ec5ce-d659-473b-a4bd-cc5a89996637" />


*Hình 2.6: Amazon CloudWatch Alarm kích hoạt báo động*

**Nhận xét:**
Sau khi hệ thống WAF ghi nhận lưu lượng tấn công vượt ngưỡng quy định, CloudWatch Alarm tự động chuyển trạng thái In alarm và gửi tín hiệu tới Lab-Security-Alerts-Topic được cài đặt mail của sinh viên.

<img width="940" height="494" alt="image" src="https://github.com/user-attachments/assets/5fa9d162-5454-4245-a0d2-69e8661ab400" />


*Hình 2.7: Mail nhận được thư cảnh báo về sự cố an ninh*

---

## IV. Đánh giá chi phí và dọn dẹp tài nguyên

### Chi phí

<img width="940" height="773" alt="image" src="https://github.com/user-attachments/assets/9c5257a4-3574-4cb2-b1cc-b5559d221c65" />


*Hình 3.1: Giao diện lab trên trang chủ đã sử dụng 12.1$ trên tổng 50$*

**Nhận xét:**
- Số dư chi phí được hiển thị thông qua hệ thống phòng lab Vocareum.
- Nhóm đã kiểm soát tốt chi phí suốt 4 tuần học, số tiền dùng thử nghiệm hệ thống vẫn nằm trong hạn mức 50$.

### Dọn dẹp tài nguyên

**Giai đoạn 1: WAF, CloudWatch, SNS, GuardDuty**
- Gỡ bỏ WAF ra khỏi Load Balancer
- Xóa các Alarm và SNS để hệ thống không gửi mail báo động nữa

**Giai đoạn 2: ALB, Target Group**
- Xóa Lab-ALB-Public
- Khi ALB đã được xóa thì mới xóa được Target Group

**Giai đoạn 3: EC2 Web Server**
- Xóa máy ảo EC2 thì ổ cứng (EBS Volume) đi kèm cũng tự mất theo.
- Kết nối từ web xuống database bị ngắt hoàn toàn

**Giai đoạn 4: RDS Database**
- Khi không còn máy ảo truy cập nữa thì xóa Database
- Không chọn “Create final snapshot” và “Retain automated backups”

**Giai đoạn 5: Security Groups**
- Xóa toàn bộ các dòng trong Inbound Rules
- Xóa các Security Groups theo thứ tự

**Giai đoạn 6: Dọn dẹp nền tảng**
- Xóa DB Subnet Group
- Dọn dẹp S3 Bucket
- Xóa Lab-VPC

---

## V. Link GitHub và Video Demo

* Link github:
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ungdung
* Link commit:
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/commit/48d4bbae80f69ed5b271f98e73fafaa7c705faa1
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/commit/4d68b9caa6a9a8e3f4427610fd160d40d41e32f2
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/commit/aa0fec2370d7c2b2c5c8d2769d2f3674eaf5b142
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/commit/69c54ea598504e301bd85282f10006ad7d54c3ff
* Link blob:
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/src/test_waf_security.ps1
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/Tuan4/BaoCaoTuan4.md
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/WORKLOG.md
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/Tuan4/DEMO.md
- https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/docs/diagram.png
* Link video:
- https://youtu.be/RNFod-LNGfU
