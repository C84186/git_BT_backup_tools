import os, bencodepy, yaml, click
from pathlib import Path

truncate_fields = []

def convert(data):
    if isinstance(data, bytes):
        if data.isascii(): return data.decode('ascii')
        return binascii.hexlify(data).decode('ascii')

    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    if isinstance(data, list):   return list(map(convert, data))
    

def parse_bencoded(bencoded_path: pathlike_hint) -> typing.Optional[dict]:
    bencoded_path = Path(bencoded_path)


    try:
        with open(bencoded_path, "rb") as f:
            decoded = bencodepy.bread(f)
    except bencodepy.exceptions.BencodeDecodeError:
        L.warn(f"{fastresume_path} failed to decode!")
        return None

    decoded = convert(decoded)
    return decoded

def print_bencoded(bencoded: typing.Optional[dict]):
    if not bencoded:
        print("---")
        print("---")
        return

    print("---")
    print(yaml.dump(bencoded))
    print("---")

