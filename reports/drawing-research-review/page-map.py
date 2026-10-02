from pypdf import PdfReader
import json,sys
p=PdfReader(sys.argv[1])
print(json.dumps({'pages':len(p.pages),'destinations':{k.lstrip('/'):p.get_destination_page_number(v)+1 for k,v in p.named_destinations.items()}}))
