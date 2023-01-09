from setuptools import setup, find_packages

setup(
    name='test-prioritization',
    version='2.0',
    url='https://github.com/Frosendroska/test-prioritization.git',
    install_requires=[
        'python-dotenv==0.21.0',
        'tqdm==4.64.1',
        'numpy==1.21.2',
        'matplotlib==3.4.3',
        'requests==2.28.1',
        'domonic==0.9.11',
        'black==22.10.0',
        'pytest',
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
