#!/usr/bin/env python3

import socket

from tencentcloud.dnspod.v20210323 import models

from __init__ import *
from lib.tencent_cloud_sdk import create_dnspod_client


def get_local_ip() -> str:
    ips = socket.gethostbyname_ex(socket.gethostname())[2]
    local_ips = list(filter(lambda ip: ip.startswith("192.168"), ips))
    if len(local_ips) != 1:
        raise Exception(f"local ip is not unique: {local_ips}")
    return local_ips[0]


def update_local_lyh543_cn(domain: str, subdomain: str, ip: str):
    full_domain = f"{subdomain}.{domain}"

    client = create_dnspod_client()
    # get record id
    request = models.DescribeRecordListRequest()
    request.Domain = domain
    request.Subdomain = subdomain
    request.RecordType = "A"
    response = client.DescribeRecordList(request)
    record_id = response.RecordList[0].RecordId
    if ip == response.RecordList[0].Value:
        print(f"{full_domain} is already {ip}")
        return

    # update record
    request = models.ModifyRecordRequest()
    request.Domain = domain
    request.SubDomain = subdomain
    request.RecordId = record_id
    request.RecordLine = "默认"
    request.RecordType = "A"
    request.Value = ip
    client.ModifyRecord(request)

    print(f"{full_domain} updated to {ip}")


if __name__ == "__main__":
    [subdomain] = argparse("subdomain", rest="error")
    local_ip = get_local_ip()
    update_local_lyh543_cn("lyh543.cn", subdomain, get_local_ip())
