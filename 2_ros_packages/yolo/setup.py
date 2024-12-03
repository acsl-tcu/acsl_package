from setuptools import setup

package_name = "yolo"

setup(
    name=package_name,
    version="0.0.0",
    packages=[],
    py_modules=[
        "src.talker",
        "src.listener",
        "src.ricoh",
        "src.pos",
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    author="student",
    author_email="student@todo.todo",
    maintainer="student",
    maintainer_email="student@todo.todo",
    keywords=["ROS", "ROS2"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Topic :: Software Development",
    ],
    description="TODO: Package description.",
    license="Apache License, Version 2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "pub= src.talker:main",
            "sub= src.listener:main",
            "ricoh = src.ricoh:main",
            "pos = src.pos:main",
        ],
    },
)
