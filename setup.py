from setuptools import setup, find_packages

# Read the contents of the README.md file
from pathlib import Path
current_directory = Path(__file__).parent
long_description = (current_directory/'README.md').read_text()

setup(
    name = 'd365fw',
    version = '0.8.1',
    packages = find_packages(),

    # Dependency
    install_requires = [
        'requests',
    ],

    # Metadata
    author = 'Yan Kuang',
    author_email = 'YTKme@Outlook.com',
    description = 'Microsoft Dynamics 365 FrameWork.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = 'GNU GENERAL PUBLIC LICENSE',
    keywords = 'dynamics d365 fw api microsoft'
)