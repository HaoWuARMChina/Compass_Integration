# Copyright © 2022 Arm China Co. Ltd. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import re

from setuptools import setup, find_packages
from distutils.core import setup
from distutils.extension import Extension
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

import AIPUBuilder


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False


__VERSION__ = AIPUBuilder.__VERSION__
__build_number__ = os.getenv("BUILD_NUMBER")
__min_pkg_path__ = os.getenv("MINIPKG_PATH")

assert __min_pkg_path__, "Cannot find mini package path (MINIPKG_PATH) in env"

if __build_number__ is not None and len(__build_number__) != 0:
    __build_number__ = ".open" + __build_number__
    __VERSION__ = __VERSION__ + str(__build_number__)
    init_file = ["AIPUBuilder", "AIPUBuilder/UnifiedParser"]
    for init_f in init_file:
        init_f = os.path.join(__min_pkg_path__, "AIPUBuilder",
                              "python", "src", init_f, "__init__.py")
        with open(init_f) as f:
            c = f.read()
            c = re.sub("__build_number__\s*=.+",
                       "__build_number__='"+__build_number__+"'", c)
        if len(c) != 0:
            with open(init_f, "w") as f:
                f.write(c)


entry_points = """
    [console_scripts]
    aipuparse = AIPUBuilder.UnifiedParser.univ_main:main
    aipuopt = AIPUBuilder.Optimizer.tools.optimizer_main:main
    aipugb = AIPUBuilder.CGBuilder:caipugb
    aipurun = AIPUBuilder.CGBuilder:caipurun
    aipubuild = AIPUBuilder.main:main
    aipubinutils = AIPUBuilder.CGBuilder:aipubinutils
    aipu_profiler = AIPUBuilder.Profiler.main:main
    """

setup(
    name="AIPUBuilder",
    version=__VERSION__,
    description="A Graph Builder for AIPU",
    author='Neo WANG',
    packages=find_packages(__min_pkg_path__ + '/AIPUBuilder/python/src'),
    package_dir={'': __min_pkg_path__ + '/AIPUBuilder/python/src'},
    package_data={
        '': [
            "*.so",
            "*.a"
        ]
    },
    install_requires=[
        "clang",
        "cloudpickle",
        "decorator",
        "editdistance",
        "future",
        "matplotlib",
        "networkx",
        "onnx>=1.11",
        "onnxoptimizer",
        "onnx-simplifier",
        "opencv-python",
        "psutil",
        "PyYAML",
        "scipy",
        "sympy",
        "synr",
        "tensorflow>=2.6"
        "tflite"
        "torch>=1.11",
        "torchvision",
        "tornado",
        "tqdm"
    ],
    cmdclass={'bdist_wheel': bdist_wheel},
    entry_points=entry_points,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
