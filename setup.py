from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='blackjack-engine',
    author='Lucas Zanini',
    author_email='zanini.lcs@gmail.com',
    license='MIT',
    keywords='python blackjack engine strategy ai',
    url='https://github.com/lzanini/blackjack-engine',
    version='0.1.4',
    description='A flexible blackjack game engine, allowing to easily implement and evaluate strategies.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['blackjack_engine', 'blackjack_engine.simulation', 'blackjack_engine.strategy'],
    python_requires='>=3.3',
    install_requires=[
        "numpy >= 1.0",
        "tqdm >= 4.0"
    ],
    extra_requires={
        "dev": [
            "pytest >= 3.7"
        ]
    }
)
