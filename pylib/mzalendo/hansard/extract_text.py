# Extract text from the xml produced from the Hansard PDF using 'pdftohtml -xml ___.pdf'

# dirty hacks:
#  * manually remove the DTD line at the top - should ignore it in the code instead.

import pprint
import xml.sax
from xml_handlers import HansardXML

filename = '/home/evdb/Hansard 01.09.11.xml'

hansard_data = HansardXML()
xml.sax.parse(filename, hansard_data)

pp = pprint.PrettyPrinter(indent=4)

print '------ content_chunks ------'
pp.pprint( hansard_data.content_chunks )