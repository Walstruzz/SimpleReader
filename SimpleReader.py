import imageio
import numpy as np
import os


class VideoReader:
    def __init__(self, filename, step=1):
        self.filename = filename
        self.capture = imageio.get_reader(filename, "ffmpeg")
        self.step = step
        self.cnt = 0

    def __call__(self):
        for i, image in enumerate(self.capture):
            if i % self.step != 0:
                continue
            yield i, self.filename, np.array(image)[..., ::-1]


class ImageReader:
    def __init__(self, filename, ext=None):
        self.ext = ext or {".jpg", ".png", ".bmp", ".avi", ".mp4"}
        self.filename = filename

    def __call__(self):
        for i in range(1):
            if os.path.splitext(self.filename)[-1].lower() in self.ext:
                image = imageio.imread(self.filename)
                yield 1, self.filename, np.array(image)[..., ::-1]


class FileReader:
    def __init__(self, filename, step=1, ext=None):
        self.filename = filename
        assert os.path.isfile(filename)
        if os.path.splitext(filename)[-1] in {".avi", ".mp4"}:
            self.reader = VideoReader(self.filename, step=step)
        else:
            self.reader = ImageReader(self.filename, ext)

    def __call__(self):
        return self.reader()


class Reader:
    def __init__(self, folder_or_file, step=1, ext=None, return_detail=False):
        self.folder = folder_or_file
        self.step = step
        self.ext = ext
        self.return_detail = return_detail

    def __call__(self):
        if os.path.isdir(self.folder):
            for root, _, files in os.walk(self.folder, False):
                for file in files:
                    file_or_video_name = os.path.join(root, file)
                    ext = os.path.splitext(file_or_video_name)[-1].lower()
                    if ext in {".mp4", ".avi"}:
                        reader = VideoReader(file_or_video_name, step=self.step)
                    else:
                        reader = FileReader(file_or_video_name, self.ext)

                    for cnt, filename, image in reader():
                        yield (cnt, file_or_video_name, filename, image) if self.return_detail else image
        else:
            reader = FileReader(self.folder, self.step, self.ext)
            for cnt, filename, image in reader():
                yield (cnt, self.folder, filename, image) if self.return_detail else image

