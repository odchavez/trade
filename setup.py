from setuptools import setup, find_packages

setup(
    name='trade',                      # Name of your package
    version='0.1',                     # Version number
    packages=find_packages(where='src'),          # Automatically find packages in your project
    package_dir={'': 'src'},              # Maps root to 'src'
    install_requires=[                 # List your package dependencies here
        # 'numpy>=1.18.0',             # Example dependency
    ],
    author='Omar Chavez',                # Your name
    author_email='chavezomard@gmail.com', # Your email
    description='A sample Python package for trade identification', # Short description of your package
    long_description=open('README.md').read(), # Long description from README file
    long_description_content_type='text/markdown',
    url='https://github.com/odchavez/trade', # URL to your package or project
    classifiers=[                      # Classifiers help users find your project by category
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',           # Minimum Python version required
)
