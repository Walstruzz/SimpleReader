from SimpleReader import Reader 


def simple_test():
    root = "SimpleReader.egg-info"
    reader = Reader(root)
    for image in reader():
        print(image.shape)


if __name__ == "__main__":
    simple_test()
    
