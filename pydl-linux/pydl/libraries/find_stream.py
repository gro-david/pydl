def main(streams):
    bitrates = [int(stream.abr.removesuffix("kbps")) for stream in streams]
    greatest_bitrate = max(bitrates)
    return streams[bitrates.index(greatest_bitrate)]
