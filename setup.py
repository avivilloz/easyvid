from setuptools import setup, find_packages

setup(
    name="video_editor",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "moviepy",
        "scipy",
    ],
    author="Aviv Illoz",
    author_email="avivilloz@gmail.com",
    description=(
        "Python package for efficient video creation, manipulation, and "
        "animation using image sequences, audio, and subtitles."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/avivilloz/video_editor",
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
