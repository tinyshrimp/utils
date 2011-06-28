'''
Created on Jan 15, 2011

@author: xiwang
'''

from setuptools import setup

setup(name='remote-desktop',
      version='0.0.1',
      author='xiwang',
      author_email='xinpengw@cn.ibm.com',
#      maintainer='',
#      maintainer_email='',
      description='The front-end of rdesktop created by wxpython.',
#      long_description='',
      url='',
#      download_url='',
#      classifiers='',
#      platforms='',
      license='',
      
      packages=['remote-desktop',
                'remote-desktop.utils'],
                
      package_dir = {'remote-desktop':'src',
                     'remote-desktop.utils':'src/utils'},
                     
#      py_modules=['remote-desktop.main', 
#                  'remote-desktop.main_dialog', 
#                  'remote-desktop.main_dialog_ui', 
#                  'remote-desktop.application'],

#      include_package_data = True,
      package_data={'remote-desktop':['README']},
      
      data_files=[('/etc/remote-desktop', ['src/config/config.xml', 'src/config/computers.xml']),
                  ('/usr/bin', ['src/remote-desktop'])],

      install_requires=['wxPython>=2.8'],
      scripts='')