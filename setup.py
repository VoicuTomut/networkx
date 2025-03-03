from setuptools import setup, find_packages

setup(
    name="networkx",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here, for example:
        # "numpy>=1.20.0",
        # "pandas>=1.3.0",
    ],
    author="Andrei Voicu Tomut ,Santiago Gimenez ,Alba ...(pleasse add youreself) ",
    author_email="tomutvoicuandrei@gmail.com",
    description="A brief description of your networkx project",
    keywords="network, graph, analysis",
    url="https://github.com/VoicuTomut/networkx.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)