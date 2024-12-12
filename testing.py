import png
import time

def main():
    
    print("PNG")
    print()

    image = png.PNG()

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

    t0 = time.time()
    image.load_file("brainbow.png")
    t1 = time.time()
    print(f"load_file function took this long to run: {t1-t0}")

    print(image.data[0:100].hex())
    print(type(image.data))
    print(len(image.data))
    print(image.info)
    print(type(image.info))
    print(len(image.info))
    print()

    t0 = time.time()
    if image.valid_png():
        print("This is a valid PNG file")
    else:
        print("This is not a valid PNG file")
    t1 = time.time()
    print()
    print(f"valid_png function took this long to run: {t1-t0}")

    t0 = time.time()
    image.read_header()
    t1 = time.time()
    print(f"read_header function took this long to run: {t1-t0}")
    
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

    t0 = time.time()
    image.read_chunks()
    t1 = time.time()
    print(f"read_chunks function took this long to run: {t1-t0}")
    
    for i in range(5):
        for j in range(6):
            print(image.img[i][j], end = " ")
        print()
    
    t0 = time.time()
    image.save_rgb("brainbow_r.png", 1)
    t1 = time.time()
    print(f"save_rgb function takes this long to run: {t1-t0}")

    help("png.PNG")

if __name__ == "__main__":
    main()