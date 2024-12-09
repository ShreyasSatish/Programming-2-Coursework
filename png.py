"""Coding Task to open a PNG, store its contents, and save modified PNG files"""
import zlib

class PNG():

    def __init__(self):
        #Initialise the PNG class with the attributes and default values
        self.data = b''
        self.info = ''
        self.width = 0
        self.height = 0
        self.bit_depth = 0
        self.color_type = 0
        self.compress = 0
        self.filter = 0
        self.interlace = 0
        self.img = []

    def load_file(self, file_name):
        #Opens a PNG file, fills out data and info attribute
        try:
            with open(file_name, mode = "rb") as f:
                self.data = f.read()
                self.info = file_name
        except FileNotFoundError:
            print("File not found")
            self.info = "file not found"

    def valid_png(self):
        #Reads the PNG signature and returns if correct values were found or not
        if self.data[0:8].hex() == "89504e470d0a1a0a":
            return True
        else:
            return False

    def read_header(self):
        #Read the image header chunk (IHDR) and updates relevant attributes
        IHDR_start_index = self.data.hex().index("49484452") + 8
        self.width = int(self.data.hex()[IHDR_start_index:IHDR_start_index + 8], 16)
        self.height = int(self.data.hex()[IHDR_start_index + 8:IHDR_start_index + 16], 16)
        self.bit_depth = int(self.data.hex()[IHDR_start_index + 16:IHDR_start_index + 18], 16)
        self.color_type = int(self.data.hex()[IHDR_start_index + 18:IHDR_start_index + 20], 16)
        self.compress = int(self.data.hex()[IHDR_start_index + 20:IHDR_start_index + 22], 16)
        self.filter = int(self.data.hex()[IHDR_start_index + 22:IHDR_start_index + 24], 16)
        self.interlace = int(self.data.hex()[IHDR_start_index + 24: IHDR_start_index + 26], 16)
    
    def read_chunks(self):
        #Reads through all chunks and updates the img attribute
        
        #Checks if data has been loaded
        if not self.data:
            print("No data has been loaded")
            return
    
        #Put all the data that starts after the IDAT header into a separate variable
        img_data = b""
        IDAT_start_index = self.data.hex().index("49444154") + 8
        IDAT_data = self.data.hex()[IDAT_start_index:]
        img_data += bytes.fromhex(IDAT_data)

        #Decompress the data, raise an error if decompression failed
        try:
            decompressed_data = zlib.decompress(img_data)
        except zlib.error as e:
            print(f"Decompression failed: {e}")
            return

        #Setting the scanline length depending on the color_type attribute
        if self.color_type == 0:
            bytes_per_pixel = 1
            stride = self.width * bytes_per_pixel
        elif self.color_type == 2:
            bytes_per_pixel = 3
            stride = self.width * bytes_per_pixel
        elif self.color_type == 4:
            bytes_per_pixel = 2
            stride = self.width * bytes_per_pixel
        elif self.color_type == 6:
            bytes_per_pixel = 4
            stride = self.width * bytes_per_pixel

        recon = []
        def recon_a(y, x): #To find recon of left bit
            return recon[y * stride + x - bytes_per_pixel] if x >= bytes_per_pixel else 0
            
        def recon_b(y, x): #To find recon of above bit
            return recon[(y - 1) * stride + x] if y > 0 else 0
            
        def recon_c(y, x): #To find recon of above left bit
            return recon[(y - 1) * stride + x - bytes_per_pixel] if y > 0 and x >= bytes_per_pixel else 0
            
        def paeth(a, b, c): #To find the paeth filter
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

            #Check if filter method is valid
            if self.filter != 0:
                print("Invalid Filter Method")
                return

            filter_type = decompressed_data[i]
            i += 1
            #Find the filter method of the scanline and undo the relevant filter
            for x in range(stride):
                filtered_x = decompressed_data[i]
                i += 1
                if filter_type == 0: #None filter
                    recon_x = filtered_x
                elif filter_type == 1: #Sub filter
                    recon_x = filtered_x + recon_a(y, x)
                elif filter_type == 2: #Up filter
                    recon_x = filtered_x + recon_b(y, x)
                elif filter_type == 3: #Average filter
                    recon_x = filtered_x + (recon_a(y, x) + recon_b(y, x)) // 2
                elif filter_type == 4: #Paeth filter
                    recon_x = filtered_x + paeth(recon_a(y, x), recon_b(y, x), recon_c(y, x))
                else:
                    print("Invalid filter type")
                recon.append(recon_x & 0xff) 
        row = [recon[i:i + 3] for i in range(0, len(recon), 3)]
        self.img = [row[i:i + self.width] for i in range(0, len(row), self.width)]

    def save_rgb(self, file_name, rgb_option):
        #Save R,G, or B channel of img attribute into PNG file called file_name
        if rgb_option not in [1, 2, 3]:
            print("Invalid rgb_option, please enter from 1, 2, or 3")
            return
        
        data = self.img
        for sublist in data:
            for entry in sublist:
                for i in range(len(entry)):
                    if i != rgb_option - 1:
                        entry[i] = 0

        flattened_list = [value for sublist in data for entry in sublist for value in entry]
        for i in range(len(flattened_list)):
            flattened_list.insert(i * self.width * 3, 0)
        channel_data = bytes(flattened_list)
        compressed_channel = zlib.compress(channel_data)

        with open(file_name, mode = "wb") as f:
            f.write(b"\x89PNG\r\n\x1a\n") #Input PNG signature
            #Write the IHDR chunk
            IHDR_data = self.data[8:33]
            f.write(IHDR_data)
            #Write the IDAT chunk
            f.write(len(compressed_channel).to_bytes(4, "big"))
            f.write(b"IDAT")
            f.write(compressed_channel)
            f.write(zlib.crc32(b"IDAT" + compressed_channel).to_bytes(4, "big"))
            #Wrtite the IEND chunk
            f.write(self.data[-12:])
        


def main():
    
    print("PNG")
    print()

    image = PNG()

    print("data:    ", image.data)
    print("info:    ", image.info)
    print("width:   ", image.width)
    print("height:  ", image.height)
    print("bit_depth:   ", image.bit_depth)
    print("color_type:  ", image.color_type)
    print("compress:    ", image.compress)
    print("filter:  ", image.filter)
    print("interlace:   ", image.interlace)
    print("img: ", image.img)

    image.load_file("brainbow.png")
    
    print(image.data[0:100].hex())
    print(type(image.data))
    print(len(image.data))
    print(image.info)
    print(type(image.info))
    print(len(image.info))
    print()

    if image.valid_png():
        print("This is a valid PNG file")
    else:
        print("This is not a valid PNG file")
    print()

    image.read_header()
    
    print("info:    ", image.info)
    print("width:   ", image.width)
    print("height:  ", image.height)
    print("bit_depth", image.bit_depth)
    print("color_type", image.color_type)
    print("compress:", image.compress)
    print("filter:  ", image.filter)
    print("interlace:", image.interlace)
    print("img: ", image.img)
    print()

    image.read_chunks()
    for i in range(5):
        for j in range(6):
            print(image.img[i][j], end = " ")
        print()
    
    image.save_rgb("brainbow_r.png", 1)

if __name__ == "__main__":
    main()