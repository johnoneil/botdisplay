from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='botdisplay',
    version='0.1',
    description='Cycle a web browser to urls determined by web interface..',
    long_description = readme(),
	classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
    keywords = 'signage large screen display broswer automation',
    url='https://github.com/johnoneil/botdisplay',
    author='John O\'Neil',
    author_email='oneil.john@gmail.com',
    license='MIT',
    packages=['botdisplay'],
    install_requires=[
        'selenium',
        'django',
        'argparse'
      ],
	package_data = {
		'webircclient': ['botdisplay/*.html', 'static/*.css','static/*.img'],
	},
    #entry_points = {
#		'console_scripts': ['botdisplay-webinte=webircclient.server:main'],
 #   },
      zip_safe=True)