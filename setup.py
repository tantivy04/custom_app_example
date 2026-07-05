from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="custom_app_example",
    version="1.0.0",
    author="Your Company",
    author_email="support@company.com",
    description="Example custom app for ERPNext multi-tenant setup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourcompany/custom_app_example",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Frappe",
    ],
    python_requires=">=3.10",
    install_requires=[
        "frappe",
    ],
    include_package_data=True,
    zip_safe=False,
)
