from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='wishful_module_ni_sdr',
    version='0.1.0',
    packages=find_packages(),
    url='http://www.wishful-project.eu/software',
    license='',
    author='Piotr Gawlowicz, Anatolij Zubow',
    author_email='{gawlowicz, zubow}@tu-berlin.de',
    description='WiSHFUL NI SDR Module',
    long_description='WiSHFUL NI SDR Module',
    keywords='wireless control',
    install_requires=[]
)
