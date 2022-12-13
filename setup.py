from setuptools import setup, find_packages

setup(
    name='test-prioritization',
    version='2.0',
    url='https://github.com/Frosendroska/test-prioritization.git',
    install_requires=[
        'python-dotenv==0.19.0',
        'tqdm==4.62.3',
        'numpy==1.21.2',
        'matplotlib==3.4.3',
        'requests==2.26.0',
        'domonic==0.7.2',
        'black==19.10b0',
        'pytest'
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
