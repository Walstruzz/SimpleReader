from setuptools import setup, find_packages 


setup(
    py_modules= ["SimpleReader"],
    packages = find_packages(),
    name =  "SimpleReader",
    version = "2.0.0",
    author = "walstruzz@outlook.com",
    install_requires = ["numpy", "imageio", "imageio-ffmpeg"],
    zip_safe = False,
    python_requires = ">=3.5",
    include_package_data = True
)
