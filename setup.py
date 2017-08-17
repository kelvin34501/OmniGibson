from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
from distutils.command.build_py import build_py as _build_py
import sys, os.path


class PostInstallCommand(install):
		"""Post-installation for installation mode."""
		def run(self):
				print('post installation')
				check_call("bash build.sh".split())
				install.run(self)


setup(name='realenv',
			description='Real Environment Developed by Stanford University',
			url='https://github.com/fxia22/realenv',
			author='Stanford University',
			zip_safe=False,
			install_requires=[
					'numpy>=1.10.4', 
					'go-vncdriver>=0.4.19',
					'pyglet>=1.2.0',
					'gym>=0.9.2'
			],
			tests_require=[],
			cmdclass={
				'install': PostInstallCommand
			}
)
