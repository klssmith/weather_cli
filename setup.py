from setuptools import find_packages, setup

setup(
    name="weather-cli",
    version="0.0.1",
    author="Katie Smith",
    description="A basic cli for the Met Office Datapoint data",
    url="https://github.com/klssmith/weather-cli",
    packages=find_packages(),
    install_requires=["requests==2.22.0", "pytz==2019.2"],
    entry_points={"console_scripts": ["weather = weather_cli.weather:main"]},
)