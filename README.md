Solution Description

The solution was implemented as a script written in Python.  It has been tested on Ubuntu 14.04.1 and Mint 17.1 but
should work with any reasonable version (+-2 major revision numbers).  Script
requires a basic standard Ubuntu/Mint install that has Internet connectivity.

To run:

1) chmod u+x auto-nginx.py
2) Execute the script as root or use sudo (it will bail otherwise).

Notes:

* Will check to make sure nginx and wget packages are installed.  If not, it'll use aptitude 
  to get them.
* Repeated runs of script will replace config files and the index.html with new ones but will   
  delete them if the contents are the same (auto cleaning!).
* Has some simple error checking via try/except loops but could use some more testing in this 
  regard.

What the script does:

1) Determines OS type.  Created some basis parts to determine if yum (RHEL derivative) or aptitude      
   (Debian/Ubuntu/Mint) should be used, but only tested to work with Ubuntu/Mint.

2) Gets index.html from Puppet github using wget.  Does some basic checking to see if a previous 
   version exists on the system.  Will save a copy (appended with current Unix time) if it does, 
   but will delete if it's the same as what was just downloaded

3) Creates a /data/www/puppet/ directory and places the index.html file in there.

4) Creates a configuration file in /etc/nginx/sites-available to serve the page.  Again, saves old
   version (appended with Unix time) and will delete if the contents are the same.  The default
   symlink is modified: /etc/nginx/sites-enabled/default -> /etc/nginx/sites-enabled/default

5) Bounces nginx.

6) Cleans up uneeded files.

Puppet Questions:

Questions

1. Describe the most difficult/painful hurdle you had to overcome in implementing your solution.

Knowing that this task could be much more easily accomplished using a configuration management
tool.  I had to use the tools that I know well, however.  Also realizing that if I wanted to get
this to work with all Linux distros, a lot more work would have to go into it.  

2. Describe which puppet related concept you think is the hardest for new users to grasp.

Realizing just how much of a game changer configuration automation really is.  A framework is being
built around automating individual server workloads to the point where they will eventually be viewed
abstractly as processes to a kernel.  We want to get away from managing individual nodes and more towards
managing resources across datacenters.  That can be a hard concept to swallow.

3. Please comment on the concept embodied by the second requirement of the solution(ii)

Auto configuration should do no harm.  That it is desirable to have a auto-configure
tool be intelligent enough to not clobber old configuration files and data haphazardly.  It is 
not only careless, but potentially dangerous to the system(s).

Also, the tool should do only as much work as required and not cause unneeded load, traffic, or bandwidth usage.  

4. Where did you go to find information to help you in the build process?

Most of the Python calls were familiar to me (basic IO, filesystem calls, etc.).  I was unfamiliar
with nginx, however, and used the Internet and Google to learn how to configure it.  Reffered to 
man pages for various things (wget etc.)

5. In a couple paragraphs explain what automation means to you and why it is important

It means to truly understand what service a system is delivering and coming up with solution can
provide it in the quickest, most efficient, and error proof manner possible.  Automating a process
not only gets you faster results more cleanly but it forces you to really understand the problem
you're trying to solve.  If you don't understand it completely, it is virtually impossible to automate.





 

to an organization's infrastructure design strategy.
