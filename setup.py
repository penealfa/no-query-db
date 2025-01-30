from setuptools import setup, find_packages

setup(
    name="noquerydb",
    version="0.0.1",
    author="Peneal Feleke",
    author_email="penealfeleke17pro@gmail.com",
    license="MIT License",
    description="A database where you just use JSON to create and interact with it",
    long_description="long_description",
    long_description_content_type="text/markdown",
    url="https://github.com/penealfa/noquerydb",
    packages=find_packages(),  # Ensure it finds your package
    include_package_data=True,  # Include extra files
    py_modules = ['no_query_db', 'app', 'orm'],
    package_data={
        "noquerydb": ["orm.py"],  # Ensure orm.py is included
    },
    install_requires= [
        "backports.tarfile==1.2.0",
        "certifi==2024.12.14",
        "charset-normalizer==3.4.0",
        "click==8.1.7",
        "colorama==0.4.6",
        "docutils==0.21.2",
        "idna==3.10",
        "importlib_metadata==8.5.0",
        "jaraco.classes==3.4.0",
        "jaraco.context==6.0.1",
        "jaraco.functools==4.1.0",  # Fixed here
        "keyring==25.5.0",
        "markdown-it-py==3.0.0",
        "mdurl==0.1.2",
        "more-itertools==10.5.0",
        "nh3==0.2.19",
        "packaging==24.2",
        "pkginfo==1.12.0",
        "Pygments==2.18.0",
        "pywin32-ctypes==0.2.3",
        "readme_renderer==44.0",
        "requests==2.32.3",
        "requests-toolbelt==1.0.0",
        "rfc3986==2.0.0",
        "rich==13.9.4",
        "twine==6.0.1",
        "urllib3==2.2.3",
        "zipp==3.21.0",
        "jsonschema==4.23.0",
        "jsonschema-specifications==2024.10.1"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        noquerydb=no_query_db:cli
    ''',
)
