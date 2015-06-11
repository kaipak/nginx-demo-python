#!/usr/bin/python
"""
    Set up basic nginx environment with simple webpage
    
    Tested with following OSes:
    -Ubuntu
    -RHEL
    
    -Kai Pak
    -16-Feb-15

"""

import os, sys, os.path, time, filecmp
from subprocess import call
from shutil import move

NGINXPKG = 'nginx'
WGETPKG = 'wget'
URL = 'https://raw.githubusercontent.com/puppetlabs/exercise-webpage/master/index.html'
APTGET = '/usr/bin/apt-get'
DPKG = '/usr/bin/dpkg'
WGET = '/usr/bin/wget'
WEBDIR = '/data/www/puppet'
PUPPETCONF = '/etc/nginx/sites-available/puppet'
NGINXDEF = '/etc/nginx/sites-enabled/default'
SERVICE =  '/usr/sbin/service'
WEBPAGE = '/data/www/puppet/index.html'
UNIXTIME = str(time.time())
DEVNULL = open(os.devnull, 'w')

# Clean up a backed up file if it's the same thing as what's replaced it
# Compare file1 to file2, if the same will delete file2.
#
def cleanup(file1, file2):
    try:
        if filecmp.cmp(file1, file2):
            print file1, 'and', file2, 'have identical content.  Deleting', file2
            os.remove(file2)
    except IOError:
        print 'File not found, skipping this clean-up step.'
    
# Get webpage from Puppet's github page
# Configure basic nginx to serve on port 8000
#
def config_nginx():
    
    # Create directory to hold page if it doesn't exist
    if not os.path.exists(WEBDIR):
        print "Creating", WEBDIR
        os.makedirs(WEBDIR)
    
    # Get index.html from Puppet github.  If file exists, replace it but save a copy.  Delete
    # if this is the same file (chksum)
    if os.path.isfile(WEBPAGE):
        print "Previous version of webpage found.  Will replace, but copy off version ending in",\
              UNIXTIME, '\n'
        move(WEBPAGE, WEBPAGE + "." + UNIXTIME)
    
    try:
        print 'Getting webpage from', URL
        call([WGET, "-P", WEBDIR, URL, "--no-check-certificate"])
    except:
        print 'Something went wrong, bailing script.'
        exit(2)
    
    # Now create nginx configuration file to serve up the webpage we just got. Copy off a version
    # if the configuration file already exists.
    if os.path.isfile(PUPPETCONF):
        print "Previous nginx config file found.  Will replace, but copy off version ending in",\
              UNIXTIME, '\n'
        move(PUPPETCONF, PUPPETCONF + "." + UNIXTIME)
    
    try:
        f = open(PUPPETCONF, 'w')
    except IOError:
        print 'Can\'t open file', PUPPETCONF
        print 'This script can\'t continue... bailing.\n'
        exit(2)
    
    f.write('server {\n')
    f.write('   listen 8000;\n')
    f.write('   location / {\n')
    f.write('       root /data/www/puppet;\n')
    f.write('   }\n')
    f.write('}\n')
    f.close()
    
    print "Linking /etc/nginx/sites-enabled/default to new configuration file..."
    os.unlink(NGINXDEF)
    os.symlink(PUPPETCONF, NGINXDEF)
    
    print "\nBouncing nginx...\n"
    call([SERVICE,NGINXPKG, "restart"])
    
    print '\nCleaning up unneeded files...\n'
    if os.path.isfile(PUPPETCONF + "." + UNIXTIME):
        cleanup(PUPPETCONF, PUPPETCONF + "." + UNIXTIME)
    if os.path.isfile(WEBPAGE + "." + UNIXTIME):
        cleanup(WEBPAGE, WEBPAGE + "." + UNIXTIME)
    
# Determine OS Type.  Very simple and not robust.  Only tested on Mint
# Ubuntu.  There's bits in there for RHEL, but this is incomplete for that family of distros.
# Mainly used to determine package manager
#
def get_OS():
    if os.path.isfile('/etc/lsb-release'):
        return 'ubuntu'
    elif os.path.isfile('/etc/redhat-release'):
        return 'rhel'
    elif os.path.isfile('/etc/centos-release'):
        return 'rhel'
    elif os.path.isfile('/etc/fedora-release'):
        return 'rhel'
    else:
        print 'This doesn\'t seem to be an OS I support (Ubuntu based).  Sorry.\n'
        exit(1)

# Install required packages depending on OS type.
# Add try blocks here
def inst_pkgs(os_type):
    print '\nChecking required packages...'
    # Package install for Debian
    if os_type == 'ubuntu':
        # Update package lists
        print 'Updating package lists...\n'
        try:
            call([APTGET, "update"])
        except:
            print "Unable to install packages. Bailing script."
            exit(2)
        
        if call([DPKG, "-s", NGINXPKG], stdout=DEVNULL, stderr=DEVNULL) != 0:
            print 'nginx appears to be missing. Installing...\n'
            try:
                call([APTGET, "-y", "install", NGINXPKG ]) #, stdout=DEVNULL, stderr=DEVNULL)
            except:
                print "Unable to install package.  Please make sure this box has Internet access."
                print "Quitting script..."
                exit(2)
        else:
            print 'nginx installed.'             
        if not os.path.isfile(WGET):
            print '\nwget appears to be missing. Installing...\n'
            try:
                call([APTGET, "-y", "install", WGETPKG]) #, stdout=DEVNULL, stderr=DEVNULL)
            except:
                print "Unable to install package.  Please make sure this box has Internet access."
                print "Quitting script..."
                exit(2)
        else:
            print 'wget installed.'
        
    elif os_type == 'rhel':
        try:
            call(["yum", "install", NGINXPKG])
        except:
            print "Unable to install packages. Bailing script."
            exit(2)
        
    print '\n\n' 
    
def main():
    # Bail if not root
    if not os.geteuid() == 0:
        sys.exit("\nMust be root to run this script\n")
        
    print "\n***Autosetup for nginx***\n" 
    
    os_type = get_OS()
    pkgmgr = ''
    os_msg = ''
    
    if os_type == 'rhel':
        pkgmgr = 'yum'
        os_msg = 'a RHEL derivative (RHEL, CentOS, Fedora, etc.). '
        print 'RHEL family distro compatibility not test... bailing.\n\n'
        exit(1)
    if os_type == 'ubuntu':
        pkgmgr = 'aptitude'
        os_msg = 'an Ubuntu derivative (Ubuntu, Mint, etc.). '
    
    print '\nYour OS appears to be', os_msg, '\nAssuming ', pkgmgr, \
          ' is your package manager.\n'
    
    inst_pkgs(os_type)
    config_nginx()
    
    print '\n\n'
    
if __name__ == '__main__':
    main()
