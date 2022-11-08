import json
import os

from pathlib import Path
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.dnspod.v20210323 import dnspod_client
from tencentcloud.dnspod.v20210323.dnspod_client import DnspodClient

for key in ["HTTP_PROXY", "HTTPS_PROXY"]:
    os.environ.pop(key, None)
os.environ["NO_PROXY"] = "*"

with open(Path("~/.tccli/default.credential").expanduser(), "r") as f:
    credential_json = json.load(f)
secret_id = credential_json["secretId"]
secret_key = credential_json["secretKey"]
cred = credential.Credential(secret_id, secret_key)


def create_dnspod_client() -> DnspodClient:
    httpProfile = HttpProfile()
    httpProfile.endpoint = "dnspod.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    return dnspod_client.DnspodClient(cred, "", clientProfile)
