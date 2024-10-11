# pip install tencentcloud-sdk-python
from pathlib import Path
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models
from tencentcloud.common.sign import Sign
import base64

def imgget(path):
    with open(path, "rb") as f:  # 转为二进制格式
        base64_data = base64.b64encode(f.read())  # 使用base64进行加密
    return base64_data.decode("utf-8")


from ocr_remote.sign import sign_tc3

Sign.sign_tc3 = staticmethod(sign_tc3)


class TencentOcr:
    secret_id = "AKIDb7NO4WCVarzNasp8f2i9LWCgniRPluIH"
    secret_key = "ItfDKctVhYYXb7Aeh7LoKET7Ccg9AEI6AFYT7MWh7IGMN/t="
    endpoint = "ocr.tencentcloudapi.com"
    region = "ap-guangzhou"
    headers = {"User-Agent": "BaiMiao/3.4.6 (iPhone; iOS 16.3; Scale/3.00)"}

    def __init__(self) -> None:
        cred = credential.Credential(self.secret_id, self.secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = self.endpoint
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        clientProfile.language = None
        client = ocr_client.OcrClient(cred, self.region, clientProfile)
        client.request_client = ""
        self.client = client

    def RecognizeTableOCR(self, params):
        req = models.RecognizeTableOCRRequest()
        req.headers = self.headers
        req.ImageBase64 = str(params)
        resp = self.client.RecognizeTableOCR(req)
        return resp
