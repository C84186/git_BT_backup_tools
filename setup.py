from setuptools import setup, find_packages

setup(
    name = 'pretty_print_bencoded',
    version = '0.0.0.9001',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'Click',
    ],
    entry_points='''
        [console_scripts]
        bencode2yaml=pretty_print:pretty_print_bencoded 
    ''',
)
