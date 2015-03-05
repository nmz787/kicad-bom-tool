import sys
import os
import getopt
import json


class cmp_to_x_converter(object):
    def __init__(self, infilepath, outfilepath, output_type='json'):
        infilepath=os.path.abspath(infilepath)
        components={}
        with open(infilepath,"r") as kicadCmpFile:
            lastline=""
            for line in kicadCmpFile:
                #the cmp file delimeter is =, get everthing after the first occurence
                value = line.split("=")[1:]
                #rejoin with = in case there was an equal sign in the value
                value = "=".join(value).strip()
                # strip the semicolon at the end if present
                if value.endswith(';'):
                    value = value[:-1]

                if line.startswith('ValeurCmp'):
                    lastValeurCmp = value

                if line.startswith('IdModule'):
                    #KiCad appends an _id
                    lastIdModule = value

                if line.startswith('Reference'):
                    lastRef = value

                if line.startswith('EndCmp'):
                    try:
                        components[(lastValeurCmp,lastIdModule)]['quantity'] += 1
                        components[(lastValeurCmp,lastIdModule)]['references'].append(lastRef)
                    except KeyError:
                        components[(lastValeurCmp,lastIdModule)] = {'quantity': 1, 'references': [lastRef] }

                    lastValeurCmp = ''
                    lastIdModule = ''
                    lastRef = ''

        self.components=[]
        #convert tuple to nested dict
        for component in components:
            self.components.append({'value':component[0], 'footprint':component[1], 'quantity': components[component]['quantity'], 'references': components[component]['references']})
        of = open(outfilepath, 'w')
        if output_type == 'json':
            of.write(json.dumps(self.components))
        elif output_type == 'csv':
            first_item = self.components[0]
            # write the column headers
            of.write('quantity,value,footprint,references\n')
            for item in self.components:
                if len(item['references'])>1:
                    refs_string = ','.join(item['references'])
                    refs_string = '"{}"'.format(refs_string)
                else:
                    refs_string = item['references'][0]
                # create the text string for the row data
                out_line = '{},{},{},{}\n'.format(item['quantity'], item['value'], item['footprint'], refs_string)
                # write the row data
                of.write(out_line)
        of.close()

def convert_to_json_then_run_browser():
        import webbrowser
        print os.path.split(__file__)
        webbrowser.open_new(os.path.abspath(os.path.join(os.path.split(__file__)[0], "main.html")))


def main2(argv):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input_file should be a KiCad .cmp file")
    parser.add_argument("output_file", help="output_file is the path for the output file (CSV or JSON)")
    parser.add_argument("output_type", help="output_type is either CSV or JSON")
    args = parser.parse_args()
    #print args
    p = cmp_to_x_converter(args.input_file, args.output_file, output_type=args.output_type.lower())


if __name__ == "__main__":
    main2(sys.argv[1:])

    