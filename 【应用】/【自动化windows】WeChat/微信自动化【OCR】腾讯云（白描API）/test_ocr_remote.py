"""
pip install --upgrade tencentcloud-sdk-python
"""

import base64
from pathlib import Path
from ocr_remote.ocr import TencentOcr,imgget

if __name__ == "__main__":
    path = r"C:\Users\13480\gitee\trade\【应用】\【自动化windows】WeChat\微信自动化【OCR】腾讯云\02-1.png"
    params = imgget(path)

    ocr = TencentOcr()
    res = ocr.RecognizeTableOCR(params)
    
    Path("./table.json").write_text(res.to_json_string(),encoding="utf-8")
    Path("./table.xlsx").write_bytes(base64.b64decode(res.Data))

    