# BÁO CÁO TIẾN ĐỘ TUẦN 3 
**Thời gian thực hiện:** 19/10/2026 – 25/10/2026  

---

## I. Worklog Phân công & Thời gian thực hiện

| Họ và tên | MSSV | Nhiệm vụ chính thực hiện | Thời gian |
| :--- | :---: | :--- | :---: |
| **Nguyễn Xuân Nhật** | 24110293 | • Khởi tạo và cấu hình AWS WAFv2 Web ACL (`Lab-ALB-WAF`), liên kết bảo vệ Application Load Balancer (`Lab-ALB-Public`). *(3.0h)*<br>• Khởi tạo kênh thông báo Amazon SNS Topic (`Lab-Security-Alerts-Topic`) và xác thực email quản trị viên. *(2.5h)*<br>• Thực nghiệm các kịch bản tấn công an ninh (SQL Injection, XSS, HTTP Flood) và ghi nhận nhật ký Sampled Requests. *(3.5h)* | **9.0 giờ** |
| **Nguyễn Công Bình** | 24110168 | • Kích hoạt dịch vụ Amazon GuardDuty tại Region `us-east-1`, tạo sample findings và phân tích mối đe dọa. *(3.0h)*<br>• Thiết lập hệ thống giám sát cảnh báo Amazon CloudWatch Alarms cho WAF Blocked Requests và hiệu năng EC2 CPU Utilization. *(2.5h)*<br>• Cấu hình các bộ quy tắc chuẩn của AWS (`AWSManagedRulesCommonRuleSet`, `AWSManagedRulesSQLiRuleSet`) và tạo custom rule `RateLimit-100`. *(2.0h)*<br>• Đóng gói mã nguồn kiểm thử tự động hóa, cấu hình CloudFormation template và cập nhật tài liệu Git. *(2.0h)* | **9.0 giờ** |

---

## II. Tích hợp, Bảo mật và Giám sát CloudWatch

### 1. Khởi tạo AWS WAFv2 Web ACL và liên kết bảo vệ ALB (Lớp 1 - Edge Security)

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/de274b9e-8d98-4e70-87da-f4066b8b8c36" />

*Hình 1.1: Khởi tạo AWS WAFv2 Web ACL (`Lab-ALB-WAF`) và liên kết bảo vệ cho Application Load Balancer (`Lab-ALB-Public`)*

* **Mục đích triển khai:**
  * Web ACL được triển khai tại tầng biên (Edge) của hệ thống mạng, gắn trực tiếp vào Application Load Balancer (ALB) để đóng vai trò bộ lọc gói tin HTTP/HTTPS trước khi dữ liệu đi vào mạng nội bộ (VPC Private Subnets).
  * Mọi truy cập vào hệ thống từ Internet đều được giám sát và kiểm tra theo thời gian thực tại lớp bảo vệ Tầng 7 (Application Layer) theo mô hình OSI.

---

### 2. Cấu hình các bộ quy tắc bảo vệ (WAF Rules & Rate Limiting)

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/a251b6b3-9435-4134-a6e4-e5c2d9796927" />

*Hình 2.1: Cấu hình các bộ quy tắc bảo vệ Managed Rules và Custom Rate-based Rule trên Web ACL*

* **Nhận xét & Phân tích cấu hình:**
  * **`AWSManagedRulesCommonRuleSet` (Core Rule Set):** Tự động nhận diện và chặn đứng các kỹ thuật khai thác lỗ hổng web phổ biến nhất (theo danh mục OWASP Top 10), bao gồm việc khai thác file command injection, path traversal, và các HTTP payload dị dạng.
  * **`AWSManagedRulesSQLiRuleSet`:** Chuyên biệt hóa việc phát hiện và vô hiệu hóa các câu lệnh truy vấn SQL độc hại cố tình chèn qua URI, Query String, Header hoặc Body.
  * **`RateLimit-100` (Custom Rule):** Thiết lập ngưỡng chặn tự động cho bất kỳ địa chỉ IP nguồn nào phát sinh vượt quá **100 requests trong cửa sổ trượt 5 phút**. Cơ chế này giúp giảm thiểu triệt để nguy cơ tấn công từ chối dịch vụ (DoS/HTTP Flood), brute-force và các công cụ quét lỗ hổng tự động.

---

### 3. Thử nghiệm tấn công và ghi nhận nhật ký (Security Testing & Logging)

#### Test Case 1: Tấn công chèn mã SQL (SQL Injection - SQLi)
* **Payload kiểm thử:** Chuỗi khai thác logic SQL `?id=1' OR 1=1--` truyền qua URL Query String.

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/05d159ae-3cf6-42b7-a37f-c241fee5d467" />

*Hình 3.1: Kiểm thử bảo mật Test Case 1 – AWS WAF ngăn chặn tấn công SQL Injection và trả về phản hồi HTTP 403 Forbidden*

* **Nhận xét:**
  * Yêu cầu chứa ký tự khai thác logic SQL (`OR 1=1`) trong query string đã kích hoạt mẫu nhận diện (signature) của bộ quy tắc `AWSManagedRulesSQLiRuleSet`.
  * Gói tin độc hại bị ngắt kết nối ngay tại tầng Load Balancer (trả về mã trạng thái `403 Forbidden`), bảo vệ cơ sở dữ liệu backend RDS không bị rò rỉ dữ liệu hoặc vượt qua cơ chế xác thực ứng dụng.

---

#### Test Case 2: Tấn công Cross-Site Scripting (XSS)
* **Payload kiểm thử:** Chèn thẻ script chứa mã độc JavaScript `<script>alert('XSS')</script>` vào tham số yêu cầu.

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/127008e2-cace-4f14-9b02-46bfe71d94e0" />

*Hình 3.2: Kiểm thử bảo mật Test Case 2 – AWS WAF ngăn chặn tấn công Cross-Site Scripting (XSS)*

* **Nhận xét:**
  * Payload chứa thẻ `<script>` thuộc danh mục mẫu tấn công đã định nghĩa sẵn trong bộ quy tắc bảo vệ cốt lõi `AWSManagedRulesCommonRuleSet`.
  * Cơ chế kiểm soát đã ngăn chặn rủi ro mã độc JavaScript được truyền xuống máy chủ web và thực thi trên trình duyệt của người dùng cuối.

---

#### Test Case 3: Tấn công từ chối dịch vụ / HTTP Flood (Rate Limiting)
* **Kịch bản kiểm thử:** Gửi dồn dập 130 requests liên tục trong thời gian ngắn tới địa chỉ DNS của Load Balancer bằng công cụ tự động.

<img width="940" height="483" alt="image" src="https://github.com/user-attachments/assets/ea1408de-565b-4860-874b-21c30ddf707d" />

*Hình 3.3: Kiểm thử bảo mật Test Case 3 – Kích hoạt quy tắc Rate Limiting (`RateLimit-100`) trên AWS WAF và ghi nhận phản hồi chặn HTTP 403 Forbidden*

* **Nhận xét:**
  * Sau khi gửi dồn dập 130 requests tới DNS của Load Balancer, bộ đếm phân tán của AWS WAF đã ghi nhận tần suất truy cập vượt ngưỡng quy định (100 requests / 5 phút).
  * Hệ thống WAF tự động kích hoạt hành động **Block**, đưa địa chỉ IP kiểm thử vào danh sách cách ly tạm thời.
  * Lệnh kiểm tra bằng `curl` ngay sau đó nhận phản hồi `HTTP/1.1 403 Forbidden` trực tiếp từ tầng biên (`Server: awselb/2.0`), chứng minh lưu lượng bất thường đã bị triệt tiêu ngay tại Load Balancer mà không làm tiêu hao tài nguyên xử lý của máy chủ web EC2.

---

#### Phân tích Nhật ký truy cập (WAF Sampled Requests)

<img width="940" height="494" alt="image" src="https://github.com/user-attachments/assets/a34e16f9-d361-4bec-a540-b816beaff74c" />

*Hình 3.4: Nhật ký WAF Sampled Requests trước khi kiểm thử – Toàn bộ lưu lượng truy cập hợp lệ được cấp phép (`Action: ALLOW`)*

<img width="940" height="503" alt="image" src="https://github.com/user-attachments/assets/01d87be4-34d0-4712-b601-2abf3e1f1343" />

*Hình 3.5: Mô phỏng kịch bản tấn công SQL Injection gửi tới hệ thống*

<img width="940" height="887" alt="image" src="https://github.com/user-attachments/assets/54536146-648e-4111-b84d-ea109f3d2cc8" />

*Hình 3.6: Nhật ký WAF Sampled Requests sau khi kiểm thử – Gói tin mang payload SQL Injection bị WAF phát hiện và kích hoạt hành động chặn (`Action: BLOCK`)*

* **Đánh giá nhật ký:**
  * WAF Sampled Requests hiển thị đầy đủ thông tin pháp chứng: Địa chỉ IP nguồn, quốc gia xuất phát, URI path, Query String, Metric Name vi phạm và Rule ID đã kích hoạt lệnh Block.

---

### 4. Kích hoạt giám sát mối đe dọa thông minh với Amazon GuardDuty

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/22fa00b5-696c-4a85-97d7-b65a221c6ef9" />

*Hình 4.1: Phân tích chi tiết cảnh báo an ninh tầng cơ sở dữ liệu (`DefenseImpairment:RDS/ModifyAuthenticationProcess`) trên giao diện Amazon GuardDuty*

* **Nhận xét & Đánh giá an ninh:**
  * Amazon GuardDuty tự động phân tích luồng nhật ký sự kiện CloudTrail và phát hiện hành vi can thiệp trái phép nhằm làm suy yếu cấu hình an ninh của cơ sở dữ liệu RDS (`RDSIAMAuthDisabled`).
  * Cơ chế giám sát liên tục (**Continuous Monitoring**) giúp phát hiện sớm nguy cơ bị hạ thấp tiêu chuẩn bảo mật (**Defense Impairment**) ngay từ bước chuẩn bị leo thang đặc quyền, cung cấp đầy đủ thông tin pháp chứng (*Finding ID, Source IP, IAM Role, Resource ARN*) để người quản trị kịp thời thu hồi quyền truy cập và bảo vệ dữ liệu.

---

### 5. Thiết lập hệ thống thông báo sự cố Amazon SNS

<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/62ed01d7-bd3d-4c42-aa16-eab8ccb6f818" />

*Hình 5.1: Khởi tạo kênh thông báo Amazon SNS (`Lab-Security-Alerts-Topic`) và xác thực đăng ký nhận cảnh báo qua Email*

* **Nhận xét:**
  * Kênh thông báo đóng vai trò trung tâm phân phối bản tin cảnh báo tự động khi phát sinh sự cố bất thường từ hệ thống giám sát.
  * Trạng thái **Confirmed** đảm bảo đường truyền liên lạc thông suốt tới quản trị viên bảo mật ngay khi có cảnh báo phát sinh từ hạ tầng đám mây.

<img width="940" height="494" alt="image" src="https://github.com/user-attachments/assets/1200089e-fd2e-4062-ae67-ed3101c6a0ed" />

*Hình 5.2: Bản tin thông báo khẩn cấp từ Amazon SNS gửi về email sinh viên xác nhận sự cố an ninh được phát hiện*

---

### 6. Cấu hình giám sát cảnh báo Amazon CloudWatch Alarms

<img width="940" height="494" alt="image" src="https://github.com/user-attachments/assets/2fc5710c-c798-4413-93ba-95ae630dde62" />

*Hình 6.1: Amazon CloudWatch Alarm chuyển sang trạng thái kích hoạt báo động (`In alarm`) khi ghi nhận sự kiện vi phạm an ninh*

* **Nhận xét:**
  * Sau khi hệ thống WAF ghi nhận lưu lượng tấn công vượt ngưỡng quy định ($\ge 5$ blocked requests trong 5 phút), CloudWatch Alarm đã tự động chuyển trạng thái đánh giá từ `OK` sang `In alarm`.
  * Hệ thống kích hoạt hành động liên kết (**Alarm Action**), gửi tín hiệu cảnh báo khẩn cấp tới kênh truyền tin Amazon SNS Topic `Lab-Security-Alerts-Topic`.

<img width="940" height="494" alt="image" src="https://github.com/user-attachments/assets/77eb2f51-a6f6-4585-a1ab-05d91d28f71b" />

*Hình 6.2: Bản tin cảnh báo sự cố an ninh tự động từ Amazon SNS gửi về hộp thư quản trị viên (`24110293@student.hcmute.edu.vn`)*

<img width="940" height="494" alt="image" src="https://github.com/user-attachments/assets/a481dd5e-1498-4d2a-804e-6b0a2c9ad693" />

*Hình 6.3: Cấu hình Amazon CloudWatch Alarm (`Lab-Alarm-EC2-HighCPUUtilization`) tự động giám sát ngưỡng quá tải vi xử lý của máy chủ web*

---

### 7. Mã nguồn IaC (Infrastructure as Code - AWS CloudFormation)

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Week 3 - AWS WAFv2 WebACL, SNS Alerts and CloudWatch Monitoring Infrastructure as Code'

Parameters:
  AdminEmail:
    Type: String
    Default: '24110293@student.hcmute.edu.vn'
    Description: 'Email address to receive critical security alarms'
  TargetALBARN:
    Type: String
    Description: 'ARN of the Application Load Balancer to associate with WAF'
    Default: 'arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/Lab-ALB-Public/50dc6c495c0c9188'
  EC2InstanceId:
    Type: String
    Description: 'EC2 Instance ID for CPU utilization monitoring'
    Default: 'i-0123456789abcdef0'

Resources:
  # 1. Amazon SNS Topic & Email Subscription
  SecurityNotificationTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: Lab-Security-Alerts-Topic

  AdminEmailSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      Endpoint: !Ref AdminEmail
      Protocol: email
      TopicArn: !Ref SecurityNotificationTopic

  # 2. AWS WAFv2 Regional Web ACL
  LabWebACL:
    Type: AWS::WAFv2::WebACL
    Properties:
      Name: Lab-ALB-WAF
      Scope: REGIONAL
      DefaultAction:
        Allow: {}
      VisibilityConfig:
        SampledRequestsEnabled: true
        CloudWatchMetricsEnabled: true
        MetricName: Lab-ALB-WAF
      Rules:
        - Name: AWS-AWSManagedRulesCommonRuleSet
          Priority: 0
          Statement:
            ManagedRuleGroupStatement:
              VendorName: AWS
              Name: AWSManagedRulesCommonRuleSet
          OverrideAction:
            None: {}
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: AWS-AWSManagedRulesCommonRuleSet

        - Name: AWS-AWSManagedRulesSQLiRuleSet
          Priority: 1
          Statement:
            ManagedRuleGroupStatement:
              VendorName: AWS
              Name: AWSManagedRulesSQLiRuleSet
          OverrideAction:
            None: {}
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: AWS-AWSManagedRulesSQLiRuleSet

        - Name: RateLimit-100
          Priority: 2
          Action:
            Block: {}
          Statement:
            RateBasedStatement:
              Limit: 100
              AggregateKeyType: IP
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: RateLimit-100

  # 3. Liên kết WAFv2 Web ACL với Application Load Balancer
  LabWebACLAssociation:
    Type: AWS::WAFv2::WebACLAssociation
    Properties:
      ResourceArn: !Ref TargetALBARN
      WebACLArn: !GetAtt LabWebACL.Arn

  # 4. CloudWatch Alarm for WAF Blocked Requests
  CloudWatchWAFBlockedAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: Lab-Alarm-WAF-BlockedRequests-High
      AlarmDescription: 'Kich hoat khi so luong request bi WAF chan vuot nguong 5 trong 5 phut'
      MetricName: BlockedRequests
      Namespace: AWS/WAFV2
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 5
      ComparisonOperator: GreaterThanOrEqualToThreshold
      Dimensions:
        - Name: Rule
          Value: ALL
        - Name: WebACL
          Value: Lab-ALB-WAF
        - Name: Region
          Value: !Ref 'AWS::Region'
      AlarmActions:
        - !Ref SecurityNotificationTopic

  # 5. CloudWatch Alarm for EC2 CPU Utilization
  CloudWatchEC2CPUAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: Lab-Alarm-EC2-HighCPUUtilization
      AlarmDescription: 'Canh bao khi tai CPU cua EC2 vuot nguong 70% lien tuc trong 5 phut'
      MetricName: CPUUtilization
      Namespace: AWS/EC2
      Statistic: Average
      Period: 300
      EvaluationPeriods: 1
      Threshold: 70
      ComparisonOperator: GreaterThanOrEqualToThreshold
      Dimensions:
        - Name: InstanceId
          Value: !Ref EC2InstanceId
      AlarmActions:
        - !Ref SecurityNotificationTopic
```

---

## III. Kho lưu trữ dự án (GitHub)
* **Đường dẫn Repository:** [https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung](https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung)
* **Link commit tuần 3:**
*  https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/commit/8e7e04951ca331192f317c3631d753f37fd5a88f
*  https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/commit/69c54ea598504e301bd85282f10006ad7d54c3ff
*  https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/commit/ae4d2ae67d30c8c7e93bae879cddc87ac9c2862e
*  **Link github blob cho các file chính:**
*  https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/Tuan3/BaoCaoTuan3.md
*  https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/WORKLOG.md
*  https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/src/test_waf_security.ps1
*  https://github.com/CongBinh-designer/Bao-mat-da-lop-cho-ung-dung/blob/main/Tuan3/waf-monitoring-template.yaml

---

## IV. Kế hoạch Tuần 4

1. **Kiểm thử tổng thể hệ thống (End-to-End Testing):**
   * Thực hiện chuỗi kịch bản kiểm thử toàn diện từ tầng biên (WAF/ALB) qua tầng ứng dụng (EC2/Secrets Manager) đến tầng dữ liệu (RDS KMS).
   * Xác thực lại toàn bộ ma trận đe dọa theo mô hình **STRIDE**.
2. **Phân tích và tối ưu hóa chi phí (Cost Optimization):**
   * Trích xuất số liệu từ **AWS Billing & Cost Explorer**.
   * Đánh giá hiệu quả của các giải pháp kiến trúc đã triển khai trong việc tiết kiệm chi phí và tối ưu hạn mức sử dụng (Free Tier / Lab Credit).
3. **Xây dựng quy trình và dọn dẹp tài nguyên (Resource Cleanup):**
   * Lập kịch bản hủy tài nguyên theo đúng thứ tự phụ thuộc (Dependency Order) để tránh phát sinh chi phí ngầm sau khi kết thúc dự án.
4. **Hoàn thiện tài liệu báo cáo tổng kết cuối kỳ:**
   * Hợp nhất toàn bộ kết quả thực nghiệm 4 tuần vào tài liệu báo cáo đồ án chính thức.
   * Đính kèm đầy đủ minh chứng kỹ thuật, cập nhật kho lưu trữ GitHub.
5. **Quay video Demo:**
   * Quay màn hình trực tiếp trình diễn kiến trúc, các kịch bản tấn công/phòng thủ thực tế và cơ chế kích hoạt cảnh báo tự động của hệ thống.
