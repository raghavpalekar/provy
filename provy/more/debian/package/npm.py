#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Roles in this namespace are meant to provision packages installed via the NPM package manager for Debian distributions.
'''

from fabric.api import settings
from provy.core import Role

from provy.more.debian.programming.nodejs import NodeJsRole

class NPMRole(Role):
    '''
    This role provides package management operations with NPM within Debian distributions.
    <em>Sample usage</em>
    <pre class="sh_python">
    from provy.core import Role
    from provy.more.debian import NPMRole

    class MySampleRole(Role):
        def provision(self):
            with self.using(NPMRole) as role:
                role.ensure_package_installed('socket.io', '0.6.17')
    </pre>
    '''


    time_format = "%d-%m-%y %H:%M:%S"
    key = 'npm-up-to-date'

    def provision(self):
        self.provision_role(NodeJsRole)

        result = None
        with settings(warn_only=True):
            result = self.execute('npm --version', stdout=False)

        if not result or 'command not found' in result:
            self.log('NPM not installed. Installing...')
            self.execute('curl http://npmjs.org/install.sh | clean=yes sh', sudo=True, stdout=False)
            self.log('NPM installed!')

    def is_package_installed(self, package_name, version=None):
        with settings(warn_only=True):
            if version:
                package_name = "%s@%s" % (package_name, version)
            return package_name in self.execute("npm --global list | egrep '%s'" % package_name, stdout=False, sudo=True)

    def ensure_package_installed(self, package_name, version=None, stdout=False, sudo=True):
        if not self.is_package_installed(package_name, version):
            if version:
                package_name = "%s@%s" % (package_name, version)

            self.log('%s is not installed (via NPM)! Installing...' % package_name)
            self.execute('npm install --global %s' % package_name, stdout=stdout, sudo=sudo)
            self.log('%s is installed (via NPM).' % package_name)
            return True
        return False
