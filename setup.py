from setuptools import setup, find_packages

from dscope import __version__

setup(
    name = "dscope",
    version = __version__,
    packages = find_packages(),
    entry_points = {
        "console_scripts": [
            "dscope=dscope.__main__:main",
        ],
    },
    install_requires=[
        # 添加依赖项
    ],
)