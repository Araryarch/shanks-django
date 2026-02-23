from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shanks-django",
    version="0.1.0",
    author="Ararya",
    author_email="araryaarch@gmail.com",
    description="Express.js-like framework built on Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ararya/shanks-django",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
    ],
    python_requires=">=3.8",
    install_requires=[
        "django>=3.2",
    ],
    keywords="django express framework web api rest",
    project_urls={
        "Bug Reports": "https://github.com/Ararya/shanks-django/issues",
        "Source": "https://github.com/Ararya/shanks-django",
        "Documentation": "https://github.com/Ararya/shanks-django#readme",
    },
)
