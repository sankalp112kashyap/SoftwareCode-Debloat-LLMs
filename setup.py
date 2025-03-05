from setuptools import setup, find_packages

setup(
    name="llm-code-debloat",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "openpyxl>=3.0.0",
        "anthropic>=0.5.0",
        "openai>=1.0.0",
        "google-generativeai>=0.3.0",
        "pytest>=7.0.0",
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "llm-debloat=main:main",
        ],
    },
    author="UC Davis MS in CS Student",
    author_email="your.email@ucdavis.edu",
    description="A tool for identifying software bloat using LLMs",
    keywords="software bloat, LLM, code optimization",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)