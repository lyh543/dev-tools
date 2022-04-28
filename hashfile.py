#!/usr/bin/env python3

from __init__ import *
import hashlib

[filename] = argparse("filename", rest="error")

content = open(filename, "rb").read()

algorithms = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512"]

for algorithm in algorithms:
    hash_method = getattr(hashlib, algorithm)
    hash_value = hash_method(content).hexdigest()
    print(f"{algorithm:6s}: {hash_value}")
