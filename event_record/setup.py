from setuptools import setup, find_packages

setup(
    name='ArtRelease',
    version='0.1.0',
    author='Your Name', # Replace with your name
    author_email='your.email@example.com', # Replace with your email
    description='An application for recording art release events.',
    long_description=open('README.md').read() if open('README.md') else '', # Optional: assumes README.md exists
    long_description_content_type='text/markdown', # Optional
    url='https://github.com/yourusername/ArtRelease', # Optional: Replace with your project URL
    packages=find_packages(), # Automatically find packages (like 'event_record' if it's a package)
    include_package_data=True, # Add this line to include data files specified in MANIFEST.in
    install_requires=[
        'pydantic>=1.9.0,<2.0.0', # From database.py
        'fastapi>=0.70.0',      # Likely used for the API
        'uvicorn[standard]>=0.15.0', # Likely used to run the FastAPI app
        # Add other dependencies here
    ],
    classifiers=[
        # Choose appropriate classifiers from https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License', # Choose your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8', # Specify minimum Python version
    entry_points={
        'console_scripts': [
            # If you have a command-line script entry point, define it here
            # 'artrelease-cli=your_module:main_function',
        ],
    },
)
