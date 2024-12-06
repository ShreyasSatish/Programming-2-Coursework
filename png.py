"""Coding Task to open a PNG, store its contents, and save modified PNG files"""


class PNG():

    def __init__(self):
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
        pass

    def valid_png(self):
        pass

    def read_header(self):
        pass

    def save_rgb(self, file_name, rgb_option):
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