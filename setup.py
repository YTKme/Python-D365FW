from setuptools import setup, find_packages

setup(
    name = "d365api",
    version = "0.7.2",
    packages = find_packages(),

    # Dependency
    install_requires = [
        "requests",
    ],

    # Metadata
    author = "Yan Kuang",
    author_email = "YTKme@Outlook.com",
    description = "Microsoft Dynamics 365 Application Programming Interface.",
    license = "GNU GENERAL PUBLIC LICENSE",
    keywords = "dynamics d365 api microsoft"
)