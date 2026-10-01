from __future__ import annotations

import json
from typing import Any

from tools._shared import ROOT, err

CATALOG_FILE = ROOT / "helpdesk_data" / "software_catalog.json"


def lookup_approved_software(software_name: str = "") -> dict[str, Any]:
    if not isinstance(software_name, str) or not software_name.strip():
        return {
            "tool": "lookup_approved_software",
            "error": "missing_software_name",
            "message": "Vui lòng cung cấp tên phần mềm cần kiểm tra.",
        }
    try:
        data = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
        query = software_name.strip().lower()
        items = data.get("software_list", [])

        matches = [
            item for item in items
            if query in item["name"].lower() or item["name"].lower() in query
        ]

        if not matches:
            return {
                "tool": "lookup_approved_software",
                "query": software_name,
                "found": False,
                "status": "not_in_catalog",
                "message": f"Phần mềm '{software_name}' không có trong danh mục được phê duyệt. Cần tạo ticket yêu cầu kiểm tra an toàn thông tin trước khi cài đặt.",
                "catalog_version": data.get("catalog_version"),
            }

        return {
            "tool": "lookup_approved_software",
            "query": software_name,
            "found": True,
            "results": matches,
            "catalog_version": data.get("catalog_version"),
        }
    except Exception as exc:
        return err("lookup_approved_software", exc)
