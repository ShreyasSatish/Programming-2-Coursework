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
        IHDR_end_index = self.data.hex().index("49484452") + 8
        self.width = int(self.data.hex()[IHDR_end_index:IHDR_end_index + 8], 16)
        self.height = int(self.data.hex()[IHDR_end_index + 8:IHDR_end_index + 16], 16)
        self.bit_depth = int(self.data.hex()[IHDR_end_index + 16:IHDR_end_index + 18], 16)
        self.color_type = int(self.data.hex()[IHDR_end_index + 18:IHDR_end_index + 20], 16)
        self.compress = int(self.data.hex()[IHDR_end_index + 20:IHDR_end_index + 22], 16)
        self.filter = int(self.data.hex()[IHDR_end_index + 22:IHDR_end_index + 24], 16)
        self.interlace = int(self.data.hex()[IHDR_end_index + 24: IHDR_end_index + 26], 16)
    
    def read_chunks(self):
        #Reads through all chunks and updates the img attribute
        IDAT_end_index = self.data.hex().index("49444154") + 8
        #IEND_end_index = self.data.hex().index("49454E44") + 8
        decompressor = zlib.decompressobj(-zlib.MAX_WBITS)
        decompressed_data = decompressor.decompress(self.data, 47)
        print(decompressed_data)

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