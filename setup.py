from setuptools import setup


with open("requirements.txt") as fp:
    requirements = fp.read()

setup(
    name="viterm",
    description="ViTerm",
    version="0.5",
    url="https://github.com/biometrical-as/viterm",
    author="Martin Hovin",
    author_email="martin@biometrical.io",
    license="MIT",
    packages=["viterm"],
    install_requires=requirements,
    # scripts=["bin/viterm"],
    entry_points={"console_scripts": ["viterm = scripts.run:app"]},
)
