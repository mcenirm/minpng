"""
http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
"""


def main():
    with open("x.png", "wb") as out:
        write_minimum_png(out)


def write_minimum_png(out):
    write_signature(out)
    write_ihdr(out)
    # write_foo(out)
    write_iend(out)


PNG_SIGNATURE = [137, 80, 78, 71, 13, 10, 26, 10]
PNG_SIGNATURE_AS_BYTES = bytes(PNG_SIGNATURE)


def write_signature(out):
    out.write(PNG_SIGNATURE_AS_BYTES)


PNG_TYPE_IHDR = b''
def write_ihdr(out):
    pass


def write_iend(out):
    pass


def write_chunk(chunk_type, chunk_data):
    length = len(chunk_data)
    crc = calculate_crc(chunk_type, chunk_data)
    write_four_byte(out, length)
    write_four_byte(out, chunk_type)
    write_chunk_data(out, chunk_data)
    write_four_byte(out, crc)


if __name__ == "__main__":
    main()
