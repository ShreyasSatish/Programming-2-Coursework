"""Coding Task to open a PNG, store its contents, and save modified PNG files"""


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
        if not self.data:
            print("No data has been loaded")
            return
        
        import zlib

        img_data = []
        IDAT_start_index = self.data.hex().index("49444154") + 8
        IDAT_length = int(self.data.hex()[IDAT_start_index - 16:IDAT_start_index - 8], 16) #Go back to find length of IDAT1 section
        IEND_finder = int(self.data.hex()[IDAT_start_index + IDAT_length + 8: IDAT_start_index + IDAT_length + 16], 16) #Check if after the IDAT1 section the IEND header is there
        IDAT_data = self.data[IDAT_start_index:IDAT_start_index + IDAT_length]
        img_data += IDAT_data
        
        while IEND_finder != "49454E44":
            IDAT_start_index += IDAT_length + 16 #Find index of next IDAT section just before data starts
            IDAT_length = int(self.data.hex()[IDAT_start_index - 16:IDAT_start_index - 8], 16)
            IEND_finder = str(self.data.hex()[IDAT_start_index + IDAT_length + 8: IDAT_start_index + IDAT_length + 16])
            IDAT_data = self.data[IDAT_start_index:IDAT_start_index + IDAT_length]
            img_data += IDAT_data
        
        try:
            decompressed_data = zlib.decompress(img_data)
        except zlib.error as e:
            print(f"Decompression failed: {e}")
            return

        # offset = 8
        # img_data = b""

        # while offset < len(self.data):
        #     chunk_length = int.from_bytes(self.data[offset:offset + 4], "big")
        #     offset += 4
        #     chunk_type = self.data[offset:offset + 4].decode("ascii")
        #     chunk_data = self.data[offset:offset + chunk_length]
        #     offset += 4
        #     if chunk_type == "IDAT":
        #         img_data += chunk_data
        #     elif chunk_type == "IEND":
        #         break
        # try:
        #     decompressed_data = zlib.decompress(img_data)
        # except zlib.error as e:
        #     print(f"Decompression failed: {e}")
        #     return

    def save_rgb(self, file_name, rgb_option):
        #Save R,G, or B channel of img attribute into PNG file called file_name
        pass


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


if __name__ == "__main__":
    main()