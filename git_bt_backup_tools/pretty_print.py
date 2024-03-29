import os, bencodepy, yaml, click, typing, binascii, zlib, logging
from pathlib import Path

logging.basicConfig(level = logging.DEBUG)
L = logging.getLogger(__name__)

pathlike_hint = typing.Union[str, bytes, os.PathLike]
truncate_fields = ['pieces']

drop_fields = {
        'active_time', 
        'seeding_time', 
        'finished_time', 
        'peers', 
        'peers6', 
        'banned_peers',
        'banned_peers6',
        'qBt-magnetUri',
        'qBt-tags',
        'trackers'
        }
def convert(data):
    if isinstance(data, bytes):
        if data.isascii(): return data.decode('ascii')
        return binascii.hexlify(data).decode('ascii')

    if isinstance(data, dict):   return dict(map(convert, data.items()))
    if isinstance(data, tuple):  return map(convert, data)
    if isinstance(data, list):   return list(map(convert, data))

    return data

def truncate_end(data):
    try:
        data = binascii.unhexlify(data)
    except binascii.Error:
        data = data.encode()
    return hex(zlib.adler32(data) & 0xffffffff)


def truncate(data: dict):
    for key in data:
        if key in truncate_fields:
            data[key] = truncate_end(data[key])

        if type(data[key]) == dict:
            data[key] = truncate(data[key])
    return data

def remove_boring(data: dict):

    return {k: v for k, v in data.items() if not  k in drop_fields}
    
def parse_bencoded(bencoded_path: pathlike_hint) -> typing.Optional[dict]:
    bencoded_path = Path(bencoded_path)


    try:
        with open(bencoded_path, "rb") as f:
            decoded = bencodepy.bread(f)
    except bencodepy.exceptions.BencodeDecodeError:
        L.warn(f"{bencoded_path} failed to decode!")
        return None

    decoded = convert(decoded)
    return decoded

def print_bencoded(bencoded: typing.Optional[dict], truncate_fields: bool, drop_boring: bool):
    if not bencoded:
        print("---")
        print("---")
        return

    if truncate_fields:
        bencoded = truncate(bencoded)

    if drop_boring:
        bencoded = remove_boring(bencoded)

    print("---")
    print(yaml.dump(bencoded))
    print("---")

@click.command()
@click.argument('bencoded_path', type = click.Path(exists = True, dir_okay = False))
@click.option('--truncate_fields', default=True, type = click.BOOL)
@click.option('--drop_boring', default=False, type = click.BOOL)
def pretty_print_bencoded(bencoded_path: pathlike_hint, truncate_fields, drop_boring):
    bencoded = parse_bencoded(bencoded_path)

    print_bencoded(bencoded, truncate_fields, drop_boring)

@click.command()
@click.argument('bencoded_path', type = click.Path(exists = True, dir_okay = False))
@click.option('--truncate_fields', default=True, type = click.BOOL)
@click.option('--drop_boring', default=True, type = click.BOOL)
def pretty_print_bencoded_fun(bencoded_path: pathlike_hint, truncate_fields, drop_boring):
    bencoded = parse_bencoded(bencoded_path)

    print_bencoded(bencoded, truncate_fields, drop_boring)
