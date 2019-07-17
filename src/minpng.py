"""
http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
"""

import zlib


def main():
    with open("x.png", "wb") as out:
        write_minimum_png(out)


PNG_SIGNATURE = [137, 80, 78, 71, 13, 10, 26, 10]
PNG_SIGNATURE_AS_BYTES = bytes(PNG_SIGNATURE)
PNG_CHUNK_TYPE_IHDR = b"IHDR"
PNG_CHUNK_TYPE_IEND = b"IEND"
PNG_CHUNK_TYPE_IDAT = b"IDAT"
PNG_COLOR_TYPE_GRAYSCALE = 0


def write_minimum_png(out):
    write_signature(out)
    width = 1
    height = 1
    bit_depth = 1
    color_type = PNG_COLOR_TYPE_GRAYSCALE
    write_ihdr(out, width, height, bit_depth, color_type)
    write_one_black_pixel(out, bit_depth, color_type)
    write_iend(out)


def write_one_black_pixel(out, bit_depth, color_type):
    if color_type == PNG_COLOR_TYPE_GRAYSCALE and bit_depth == 1:
        scanlines = bytes([0])
    write_idat(out, scanlines, filter_none)


def write_signature(out):
    out.write(PNG_SIGNATURE_AS_BYTES)


def write_ihdr(out, width, height, bit_depth, color_type):
    data = b"".join(
        [
            four_byte(width),
            four_byte(height),
            one_byte(bit_depth),
            one_byte(color_type),
            one_byte(
                0
            ),  # deflate/inflate compression with a sliding window of at most 32768 bytes
            one_byte(0),  # adaptive filtering with five basic filter types
            one_byte(0),  # no interlace
        ]
    )
    write_chunk(out, PNG_CHUNK_TYPE_IHDR, data)


def write_iend(out):
    write_chunk(out, PNG_CHUNK_TYPE_IEND, b"")


def write_idat(out, scanlines, filter):
    data1 = filter(scanlines)
    data2 = zlib.compress(data1)
    write_chunk(out, PNG_CHUNK_TYPE_IDAT, data2)


def filter_none(scanlines):
    return b"\0" + scanlines


def four_byte(i):
    return to_bytes(i, 4)


def one_byte(i):
    return to_bytes(i, 1)


def to_bytes(i, length):
    return int(i).to_bytes(length, "big", signed=False)


def write_chunk(out, chunk_type, chunk_data):
    length = len(chunk_data)
    crc = calculate_crc(chunk_type, chunk_data)
    out.write(four_byte(length))
    out.write(bytes(chunk_type))
    out.write(chunk_data)
    out.write(four_byte(crc))


def calculate_crc(chunk_type, chunk_data):
    c1 = zlib.crc32(chunk_type)
    c2 = zlib.crc32(chunk_data, c1)
    return c2


def write_four_byte(out, word):
    out.write(word)


def write_chunk_data(out, data):
    out.write(data)


if __name__ == "__main__":
    main()
