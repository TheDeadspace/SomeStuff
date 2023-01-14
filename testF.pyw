import os
import sys

def Prop(args):

	if args[1] == 'Hide':
		os.system("attrib +H +S Log")
	elif args[1] == 'Unhide':
		os.system("attrib -H -S Log")



if __name__ == "__main__":
    Prop(sys.argv)