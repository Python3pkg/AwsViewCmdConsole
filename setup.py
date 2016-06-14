from distutils.core import setup

setup(
    name='AwsViewCmdConsole',
    version='1.0',
    packages=['awscore'],
    scripts=['scripts/awsview'],
    url='',
    license='MIT',
    install_requires=['boto3', 'prettytable'],

    entry_points={
        'console_scripts': [
            'awsview=awsview:main',
        ],
    },

    author='Ajeesh T Vijayan',
    author_email='ajeeshvt@gmail.com',
    description='A simple python application to view the AWS account resources in a tabular format'
)
