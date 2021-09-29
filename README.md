# A Simple Image/Video Reader Without OpenCV


## Usage
```python
from SimpleReader import Reader


reader = Reader("filename/folder/")
for cnt, folder, filename, image in reader():
    # image: (H, W, C), BGR format
    pass 
```

## TODO
* More TEST
* Output RGB/RGBA instead of BGR


##  License
MIT License
