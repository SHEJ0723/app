from setuptools import setup, find_packages

setup(
    name="parking-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cors',
        'flask-jwt-extended',
        'flask-sqlalchemy',
        'pymysql',
        'python-dotenv',
        'redis'
    ]
) 