from setuptools import find_packages, setup

package_name = "novel_python_node"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="iehtian",
    maintainer_email="iehtian@qq.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "novel_python_node = novel_python_node.novel_python_node:main",
            "novel_reader = novel_python_node.read:main",
        ],
    },
)
