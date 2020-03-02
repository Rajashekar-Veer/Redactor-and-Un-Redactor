from setuptools import setup, find_pakages

setup(
        name ='project0',
        version='1.0',
        author= 'Rajashekar Veerabhadra',
        author_email='Rajashekar.v@ou.edu',
        packages=find_packages(exclude=('tests','docs')),
        setup_requires=['pytest_runner'],
        tests_requires=['pytest']

)
