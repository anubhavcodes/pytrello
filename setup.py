from setuptools import setup, find_packages

setup(
    name="create_trello_cards",
    version="0.0.1",
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    setup_requires=['pytest-runner'],
    test_require=['pytest'],
    install_requires=[
        "requests",
        "bs4",
        "click",
        "pony",
        "xmltodict"
    ],
    entry_points={
        "console_scripts": [
            "create_trello_cards=create_trello_cards.__main__:main"
        ]
    },
)