from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith('#')]

setup(
    name="calendar_ai_bot",
    version="0.1.0",
    author="AI Integration Tools Team",
    author_email="example@example.com",
    description="An AI-powered Google Calendar bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/calendar-ai-bot",
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Scheduling",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "calendar-ai-bot=calendar_ai_bot.app:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
            "mypy"
        ]
    },
    keywords="calendar ai bot google automation scheduling",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/calendar-ai-bot/issues",
        "Source": "https://github.com/yourusername/calendar-ai-bot",
    },
)
