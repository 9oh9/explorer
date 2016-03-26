from setuptools import setup, find_packages
setup(
    name = "Uber Project",
    version = "0.0.1",
    packages = find_packages(),

    # requirements
    install_requires = [
        'Flask==0.10.1',
        'GeoAlchemy2==0.2.6',
        'itsdangerous==0.24',
        'Jinja2==2.8',
        'MarkupSafe==0.23',
        'psycopg2==2.6.1',
        'SQLAlchemy==1.0.12',
        'Werkzeug==0.11.5',
        'wheel==0.24.0'
    ],
    scripts=['bin/csvwriter.py'],

    # metadata for upload to PyPI
    author = "Brent Rotz",
    author_email = "rotzbrent@gmail.com",
    description = "Uber Full Stack Project",
)
