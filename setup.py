from distutils.core import setup

setup(
    name='AwsViewCmdConsole',
    version='1.0',
    packages=['core'],
    url='',
    license='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='aws command line tool',
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
