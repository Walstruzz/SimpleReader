import imageio
import numpy as np
import os
import pdb

def _get_lower_ext(name):
    return os.path.splitext(name)[-1].lower()
    
    
class VideoReader:
    @staticmethod
    def default_ext():
        return {".avi", ".mp4", ".ts", ".flv"}

    def __init__(self, filename, step=1, ext=None):
        self.ext = ext or self.default_ext()
        self.filename = filename
        if _get_lower_ext(self.filename) in self.ext:
            self.capture = imageio.get_reader(filename, "ffmpeg")
        else:
            self.capture = []
        self.step = step
        self.cnt = 0

    def __call__(self):
        for i, image in enumerate(self.capture):
            if i % self.step != 0:
                continue
            yield i, self.filename, np.array(image)[..., ::-1]


class ImageReader:
    @staticmethod
    def default_ext():
        return {".jpg", ".png", ".bmp"}

    def __init__(self, filename, ext=None):
        self.ext = ext or self.default_ext()
        self.filename = filename

    def __call__(self):
        for i in range(1):
            if _get_lower_ext(self.filename) in self.ext:
                image = imageio.imread(self.filename)
                yield 1, self.filename, np.array(image)[..., ::-1]


class EmptyReader:
    def __init__(self, *args, **kwargs):
        pass 

    def __call__(self):
        for _ in range(0):
            yield None


class FileReader:
    def __init__(self, filename, step=1, image_ext=None, video_ext=None):
        self.filename = filename
        assert os.path.isfile(filename)
        file_ext = _get_lower_ext(filename)
        if file_ext in (video_ext or VideoReader.default_ext()):
            self.reader = VideoReader(self.filename, step=step, ext=video_ext)
        elif file_ext in (image_ext or ImageReader.default_ext()):
            self.reader = ImageReader(self.filename, ext=image_ext)
        else:
            self.reader = EmptyReader()

    def __call__(self):
        return self.reader()


class Reader:
    def __init__(self, folder_or_file, step=1, return_detail=False, image_ext=None, video_ext=None):
        self.folder = folder_or_file
        self.step = step
        self.return_detail = return_detail
        self.image_ext = image_ext
        self.video_ext = video_ext

    def __call__(self):
        if os.path.isdir(self.folder):
            for root, _, files in os.walk(self.folder, False):
                for file in files:
                    file_or_video_name = os.path.join(root, file)
                    reader = FileReader(file_or_video_name, step=self.step, image_ext=self.image_ext, video_ext=self.video_ext)
                    for cnt, filename, image in reader():
                        yield (cnt, file_or_video_name, filename, image) if self.return_detail else image
        else:
            reader = FileReader(self.folder, self.step, self.image_ext, self.video_ext)
            for cnt, filename, image in reader():
                yield (cnt, self.folder, filename, image) if self.return_detail else image

