import sys
import os
import getopt
import json

def get_new_octopart_component():
	component = {"mpn":"", "quantity":0}
	return component

def read_kicad_cmp(kicadCmpFilePath):
		with open(kicadCmpFilePath, "r") as kicadCmpFile:
			lastItem


class cmp_to_csv_converter(object):
	def __init__(self, infilepath, outfilepath):
		infilepath=os.path.abspath(infilepath)
		components={}
		with open(infilepath,"r") as kicadCmpFile:
			lastline=""
			for line in kicadCmpFile:
				#the cmp file delimeter is =, get everthing after the first occurence
				value = line.split("=")[1:]
				#rejoin with = in case there was an equal sign in the value
				value = "=".join(value).strip()
				if "ValeurCmp" in line:
					lastValeurCmp = value
				if "IdModule" in line:
					#KiCad appends an _id
					lastIdModule = value
				if "EndCmp" in line:
					try:
						components[(lastValeurCmp,lastIdModule)] += 1
					except KeyError:
						components[(lastValeurCmp,lastIdModule)] = 1
					lastValeurCmp = ""
					lastIdModule = ""
		self.components=[]
		#convert tuple to nested dict
		for component in components:
			self.components.append({"value":component[0], "footprint":component[1], "quantity": components[component]})
		of = open(outfilepath, 'w')
		of.write(json.dumps(self.components))
		of.close()
		import webbrowser
		print os.path.split(__file__)
		webbrowser.open_new(os.path.abspath(os.path.join(os.path.split(__file__)[0], "main.html")))

def main(argv):
	inputfile = ''
	outputfile = ''
	thisFileName = os.path.split(__file__)[1]
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print '%s -i <inputfile> -o <outputfile>' % thisFileName
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print '%s -i <inputfile> -o <outputfile>' % thisFileName
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
	print 'Input file is "', inputfile
	print 'Output file is "', outputfile
	p=cmp_to_csv_converter(inputfile, outputfile)

def main2(argv):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("inputfile", help="inputfile should be a KiCad .cmp file")
	parser.add_argument("outputfile", help="outputfile is the path for the output CSV file")
	args = parser.parse_args()
	#print args
	p=cmp_to_csv_converter(args.inputfile, args.outputfile)


if __name__ == "__main__":
	main2(sys.argv[1:])

	