---
name: lookup_approved_software
track: bonus
kind: local_inventory
provider: mock_software_catalog
requires_env: []
inputs: [software_name]
outputs: [query, found, results, catalog_version]
side_effect: false
---
# lookup_approved_software

Tra cứu danh mục phần mềm được phê duyệt (Approved Software Catalog) của công ty.
Nhận vào tên phần mềm và trả về trạng thái phê duyệt (approved, restricted, banned),
phiên bản cho phép, phương thức cài đặt (Self-Service Portal hoặc cần duyệt ngoại lệ)
và các khuyến nghị bảo mật.
Tool này không tải xuống hoặc cài đặt phần mềm thật lên thiết bị.
