for y in range(0, self.height):

            #Check if filter method is valid
            if self.filter != 0:
                print("Invalid Filter Method")
                return

            img_array = []
            filter_type = decompressed_data[y * scanline_length]
            scanline = decompressed_data[y * scanline_length + 1: (y + 1) * scanline_length]
            reconstructed_scanline = bytearray(len(scanline))

            #Find the filter method of the scanline and undo the relevant filter
            if filter_type == 0:
                img_array.append(scanline)
            elif filter_type == 1:
                for x in range(len(scanline)):
                    if x < bytes_per_pixel:
                        reconstructed_scanline[x] = scanline[x]
                    else:
                        reconstructed_scanline[x] = (scanline[x] + reconstructed_scanline[x - bytes_per_pixel]) % 256
                img_array.append(reconstructed_scanline)
            elif filter_type == 2:
                for x in range(len(scanline)):
                    if x == 0:
                        prev_scanline = scanline
                        img_array.append(scanline)
                    else:
                        reconstructed_scanline[x] = (scanline[x] + prev_scanline[x]) % 256
                img_array.append(reconstructed_scanline)
            elif filter_type == 3:
                for x in range(len(scanline)):
                    if x <= bytes_per_pixel:
                        prev_scanline = scanline
                        reconstructed_scanline[x] = (scanline[x] + (prev_scanline[x]) // 2) % 256
                    else:
                        left = reconstructed_scanline[x - bytes_per_pixel]
                        reconstructed_scanline[x] = (scanline[x] + (left + prev_scanline[x]) // 2) % 256
                img_array.append(reconstructed_scanline)
            elif filter_type == 4:
                def paeth_predictor(a, b, c):
                    p = a + b - c
                    pa = abs(p - a)
                    pb = abs(p - b)
                    pc = abs(p - c)
                    if pa <= pb and pa <= pc:
                        return a
                    elif pb <= pc:
                        return b
                    else:
                        return c

                for x in range(len(scanline)):
                    if x <= bytes_per_pixel:
                        prev_scanline = scanline
                        prev_left = prev_scanline[x - bytes_per_pixel]
                        reconstructed_scanline[x] = (scanline[x] + paeth_predictor(0, prev_scanline[x], prev_left)) % 256
                    else:
                        prev_left = prev_scanline[x - bytes_per_pixel]
                        left = reconstructed_scanline[x - bytes_per_pixel]
                        reconstructed_scanline[x] = (scanline[x] + paeth_predictor(left, prev_scanline[x], prev_left)) % 256
                img_array.append(reconstructed_scanline)
            else:
                print(f"Unrecognised filter type: {filter_type}")