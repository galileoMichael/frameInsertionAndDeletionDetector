def extract_macroblocks(frame):
    if frame is not None:
        height, width, _ = frame.shape
        block_size = 16
        macroblocks = []

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                macroblock = frame[y:y + block_size, x:x + block_size]
                if macroblock.shape[:2] == (block_size, block_size):
                    macroblocks.append(macroblock)

        return macroblocks
    else:
        print("Frame not found or could not be read.")
        return None