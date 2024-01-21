from setuptools import setup, find_packages

setup(
    name='COMP-4453 chatbot project',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'start_app=app:main',
        ],
    },
)
