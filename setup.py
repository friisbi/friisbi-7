from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="friisbi",
    version="0.0.1",
    description="RSS Feed Reader for Frappe - Flipboard-style reader with multi-user support",
    author="Friisbi Team",
    author_email="info@friisbi.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
