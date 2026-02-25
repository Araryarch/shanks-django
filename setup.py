from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shanks-django",
    version="0.2.2",
    author="Ararya",
    author_email="araryaarch@gmail.com",
    description="Express.js-like framework built on Django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ararya/shanks-django",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*", "example-project", "docs-website", "vscode-extension"]),
    include_package_data=True,
    package_data={
        "shanks": ["templates/*.html"],
    },
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
        "black>=23.0.0",
        "watchdog>=3.0.0",
    ],
    extras_require={
        "postgres": ["psycopg2-binary>=2.9.0"],
        "mysql": ["mysqlclient>=2.1.0"],
        "mongodb": ["pymongo>=4.0.0"],
        "redis": ["redis>=4.0.0"],
        "all": [
            "psycopg2-binary>=2.9.0",
            "mysqlclient>=2.1.0",
            "pymongo>=4.0.0",
            "redis>=4.0.0",
            "dj-database-url>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "shanks=shanks.cli:main",
            "sorm=shanks.cli:sorm_main",
        ],
    },
    keywords="django express framework web api rest",
    project_urls={
        "Bug Reports": "https://github.com/Araryarch/shanks-django/issues",
        "Source": "https://github.com/Araryarch/shanks-django",
        "Documentation": "https://github.com/Araryarch/shanks-docs#readme",
    },
)
