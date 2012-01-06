import Pyro.core
import sys, shutil


controller = Pyro.core.getProxyForURI(open('uri', 'r').read())

command = sys.argv[1]
if (command == '-am'):
    controller.d.add_from_ml(sys.argv[2])
    open('links', 'w+').write(sys.argv[2])

if (command == '-af'):
    print type(controller.d)
    #controller.d.add_from_file(sys.argv[2])
    #shutil.copyfile(sys.argv[2], 'resume/'+sys.argv[2].split('/')[-1])