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
        #Opens a PNG file, and fills out data attribute
        try:
            self.data = open(file_name)
            self.info = file_name
        except FileNotFoundError:
            print("File not found")
            self.info = "file not found"

    def valid_png(self):
        #Reads the PNG signature and returns if correct values were found or not
        pass

    def read_header(self):
        #Read the image header chunk (IHDR) and updates relevant attributes
        pass

    def read_chunks(self):
        #Reads through all chunks and updates the img attribute
        pass

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


if __name__ == "__main__":
    main()