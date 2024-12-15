from setuptools import setup, find_packages

print("Packages where src is are found in : ")
print(find_packages(where="src"))
setup(
    name="cli-reader",
    version="1.0",
    description="Read formatted files in the terminal",
    author="dar",
    url="https://github.com/davidrose07/cli_reader",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "reader=cli_reader.main:main"
        ]
    },
    install_requires=[
        "colorama==0.4.6",
        "numpy==1.25.0",
        "pandas==2.2.2",
        "prompt_toolkit==3.0.47",
        "python-dateutil==2.9.0.post0",
        "pytz==2024.1",
        "six==1.16.0",
        "tabulate==0.9.0",
        "tzdata==2024.1",
        "wcwidth==0.2.13"
    ],
)
