from setuptools import setup, find_packages
from os import path
import pkg_resources

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt')) as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='mail2gg',
    version='0.1.5',
    packages=find_packages(),
    description='Import mail to Google Groups using an IMAP account or mbox file',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/XaviTorello/mail2gg',
    download_url='https://github.com/XaviTorello/mail2gg/archive/master.zip',
    project_urls={
        'Bug Reports': 'https://github.com/XaviTorello/mail2gg/issues',
        'Source': 'https://github.com/XaviTorello/mail2gg',
        'Download': 'https://github.com/XaviTorello/mail2gg/archive/master.zip',
    },
    author='Xavi Torelló',
    author_email='info@xaviertorello.cat',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        'Environment :: Console',
        'Topic :: Communications :: Email',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',

        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3',
    ],
    keywords='mail importer googlegroups google groups imap mbox migrate',

    python_requires='>=3.5, <4',
    install_requires=install_requires,

    entry_points={
        'console_scripts': [
            'imap2gg = mail2gg.cli:execute_imap_importer',
            'mbox2gg = mail2gg.cli:execute_mbox_importer',
        ]
    }
)
