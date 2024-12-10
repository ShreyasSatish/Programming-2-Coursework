"""Coding Task to open a PNG, store its contents, and save modified PNG files"""
import zlib

class PNG():
    """
    A class to handle PNG files.
    
    Attributes
    ----------
    data : bytes.
        The full raw data of the PNG.
    info : str.
        Takes the value of the file name or becomes 'File not found' if an error occurs.
    width : int.
        The width of the loaded PNG.
    height : int.
        The height of the loaded PNG.
    bit_depth : int.
        The bit depth of the loaded PNG.
    color_type : int.
        The color type of the loaded PNG.
    compress : int.
        The compression method of the loaded PNG.
    filter : int.
        The filter method of the loaded PNG.
    interlace : int.
        The interlace method of the loaded PNG.
    img : list.
        The decompressed data in the IDAT chunk of the loaded PNG.
    """

    def __init__(self, data = b'', info = '', width = 0, height = 0,
                 bit_depth = 0, color_type = 0, compress = 0, 
                 filter = 0, interlace = 0, img = []):
        """Initialises the instance based on input parameters.
        
        Returns None.
        """
        
        self.data = data
        self.info = info
        self.width = width
        self.height = height
        self.bit_depth = bit_depth
        self.color_type = color_type
        self.compress = compress
        self.filter = filter
        self.interlace = interlace
        self.img = img

    def load_file(self, file_name):
        """Opens a PNG file, fills out data and info attribute.
        
        Args:
            file_name: File name or file path to be opened.
        
        Returns None.
        """

        try:
            with open(file_name, mode = "rb") as f:
                self.data = f.read()
                self.info = file_name
        except FileNotFoundError:
            print("File not found")
            self.info = "file not found"

    def valid_png(self):
        """Reads the PNG signature to determine if loaded file is valid.
        
        Returns True/False.
        """

        if self.info == "file not found":
            print(self.info)
            return
        elif self.data[0:8].hex() == "89504e470d0a1a0a":
            return True
        else:
            return False

    def read_header(self):
        """Reads the IHDR chunk and fills out relevant attributes.
        
        Returns None.
        """
        if not self.valid_png():
            print("Loaded file is not a valid PNG")
            return

        IHDR_start_index = self.data.hex().index("49484452") + 8
        self.width = int(self.data.hex()[IHDR_start_index:IHDR_start_index + 8], 16)
        self.height = int(self.data.hex()[IHDR_start_index + 8:IHDR_start_index + 16], 16)
        self.bit_depth = int(self.data.hex()[IHDR_start_index + 16:IHDR_start_index + 18], 16)
        self.color_type = int(self.data.hex()[IHDR_start_index + 18:IHDR_start_index + 20], 16)
        self.compress = int(self.data.hex()[IHDR_start_index + 20:IHDR_start_index + 22], 16)
        self.filter = int(self.data.hex()[IHDR_start_index + 22:IHDR_start_index + 24], 16)
        self.interlace = int(self.data.hex()[IHDR_start_index + 24: IHDR_start_index + 26], 16)
    
    def read_chunks(self):
        """Reads through IDAT chunk and decompresses data within chunk.
        Undoes filtering on scanlines and stores data in img attribute.

        Returns None.
        """

        # Checks if data has been loaded
        if not self.valid_png():
            print("Loaded file is not a valid PNG")
            return
        elif not self.data:
            print("No data has been loaded")
            return
    
        # Put all the data that starts after the IDAT header into a separate variable
        img_data = b""
        i = 8
        
        while i < len(self.data):
            # Read chunk length
            chunk_len = int.from_bytes(self.data[i:i + 4], "big")
            i += 4
            # Read the chunk type
            chunk_type = self.data[i:i + 4]
            i += 4
            # Read the chunk data, based on chunk length
            chunk_data = self.data[i:i + chunk_len]
            i += chunk_len
            # Step over CRC
            i += 4
            # Want to process only the IDAT chunks
            if chunk_type == b"IDAT":
                img_data += chunk_data
            elif chunk_type == b"IEND":
                break

        # Decompress the data, raise an error if decompression failed
        try:
            decompressed_data = zlib.decompress(img_data)
        except zlib.error as e:
            print(f"Decompression failed: {e}")
            return

        stride= self.width * 3
        recon = []
        def recon_a(y, x): # To find reconstruction of left bit
            return recon[y * stride + x - 3] if x >= 3 else 0
            
        def recon_b(y, x): # To find reconstruction of above bit
            return recon[(y - 1) * stride + x] if y > 0 else 0
            
        def recon_c(y, x): # To find reconstruction of above left bit
            return recon[(y - 1) * stride + x - 3] if y > 0 and x >= 3 else 0
            
        def paeth(a, b, c): # To find reconstruction of paeth filter
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

        i = 0
        for y in range(0, self.height):
            # Check if filter method is valid
            if self.filter != 0:
                print("Invalid Filter Method")
                return
            filter_type = decompressed_data[i]
            i += 1
            # Find the filter method of the scanline and undo the relevant filter
            for x in range(stride):
                filtered_x = decompressed_data[i]
                i += 1
                if filter_type == 0: # None filter
                    recon_x = filtered_x
                elif filter_type == 1: # Sub filter
                    recon_x = filtered_x + recon_a(y, x)
                elif filter_type == 2: # Up filter
                    recon_x = filtered_x + recon_b(y, x)
                elif filter_type == 3: # Average filter
                    recon_x = filtered_x + (recon_a(y, x) + recon_b(y, x)) // 2
                elif filter_type == 4: # Paeth filter
                    recon_x = filtered_x + paeth(recon_a(y, x), recon_b(y, x), recon_c(y, x))
                else:
                    print("Invalid filter type")
                recon.append(recon_x & 0xff) 
        row = [recon[i:i + 3] for i in range(0, len(recon), 3)]
        self.img = [row[i:i + self.width] for i in range(0, len(row), self.width)]

    def save_rgb(self, file_name, rgb_option):
        # Save R, G, or B channel of img attribute into PNG file called file_name
        """Picks out desired channel and saves it into a seperate file.
        
        Args:
            file_name: File name of new file to be made.
            rgb_option: RGB channel to be picked out and saved.
                        1, 2, 3 -> R, G, B.
        
        Returns None
        """
        if not self.valid_png():
            print("Loaded file is not a valid PNG")
            return
        elif not self.data:
            print("No data has been loaded")
            return
        elif rgb_option not in [1, 2, 3]:
            print("Invalid rgb_option, please enter from 1, 2, or 3")
            return
        
        # Create a copy of self.img
        channel_img = []
        for scanline in self.img:
            channel_scanline = []
            for pixel in scanline:
                # Zero out colour channels apart from the selected one
                new_pixel = [0, 0, 0]
                new_pixel[rgb_option - 1] = pixel[rgb_option - 1]
                channel_scanline.append(new_pixel)
            channel_img.append(channel_scanline)

        # Add a filter byte at the start of each scanline
        # Filter byte is 0 for simplicity
        raw_data = bytearray()
        for scanline in channel_img:
            raw_data.append(0)
            for pixel in scanline:
                raw_data.extend(pixel)
        
        # Compress the data using the zlib format
        compressed_data = zlib.compress(bytes(raw_data))

        # Prepare the basic PNG file structure
        with open(file_name, mode = "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n") # Input PNG signature
            # Write the IHDR chunk
            IHDR_data = self.data[8:33]
            f.write(IHDR_data)
            # Write the IDAT chunk
            f.write(len(compressed_data).to_bytes(4, "big"))
            f.write(b"IDAT")
            f.write(compressed_data)
            f.write(zlib.crc32(b"IDAT" + compressed_data).to_bytes(4, "big"))
            # Wrtite the IEND chunk
            f.write(self.data[-12:])
            