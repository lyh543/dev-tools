#!/usr/bin/env python3

import socket
import click

from tencentcloud.dnspod.v20210323 import models

from __init__ import *
from lib.tencent_cloud_sdk import create_dnspod_client


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("www.baidu.com", 443))
    local_ip = s.getsockname()[0]
    s.close()
    if not local_ip.startswith("192.168."):
        raise Exception("local ip is not 192.168.*")
    return local_ip


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


@click.command()
@click.argument("subdomain")
def main(subdomain: str):
    local_ip = get_local_ip()
    update_local_lyh543_cn("lyh543.cn", subdomain, get_local_ip())


if __name__ == "__main__":
    main()
