"""
Ce fichier fait partie de LulzExpress.

    LulzExpress est un logiciel libre : vous pouvez le redistribuer
    ou le modifier selon les termes de la GNU General Public
    License tels que publiés par la Free Software
    Foundation : à votre choix, soit la version 3 de la licence,
    soit une version ultérieure quelle qu'elle soit.

    LulzExpress est distribué dans l'espoir qu'il sera utile, mais
    SANS AUCUNE GARANTIE ; sans même la garantie implicite de
    QUALITÉ MARCHANDE ou D'ADÉQUATION À UNE UTILISATION
    PARTICULIÈRE. Pour plus de détails, reportez-vous à la GNU
    General Public License.

    Vous devez avoir reçu une copie de la GNU General Public
    License avec ce programme. Si ce n'est pas le cas, consultez
    <http://www.gnu.org/licenses/>] 
"""

from xml.dom.minidom import parse
import urllib.request

def xmldownload(url,site):
  """ Fonction qui télécharge la source XML et retourne le fichier """ 
	page = urllib.request.urlopen(url)
	encod="utf-8"
	#Special case for PEBKAC, where the encoding is a little different
	if (site=="PBK"):
		encod="ISO-8859-1"
		
	infos = str(page.read(), encod)
	xmlfile=open(site+".xml","w")
	xmlfile.write(infos)
	xmlfile.close()
	xmlfile=open(site+".xml","r")	
	return xmlfile

def conversionHTML(st):
	""" Fonction de conversion des caractères HTML, à défaut de mieux :/ """
	st=st.replace("&amp;lt;","<")
	st=st.replace("&amp;gt;",">")
	st=st.replace("&amp;quot;",'"')
	st=st.replace("&lt;br /&gt;\n","\n")
	st=st.replace("&lt;br /&gt;","")
	st=st.replace("&quot;",'"')
	
	return st
def parser(xmlf, site):
	""" Parser généralisé pour les trois sites """
	stmp=""
	listoutput=[]
	#Parsing du fichier
	tmp=parse(xmlf)
	quoteslist=[]
	#Mots clés à parser
	keywordparsing=["description","description","content"]
	#Parsing des quotes
	for node in tmp.getElementsByTagName(keywordparsing[site]):
		quoteslist.append(node.toxml())
	#Traitement de la liste parsée
	#Il faut : pour chaque quote délimiter la vraie quote ainsi que faire la conversion des caractères HTML ou ISO8859-1
	for quote in quoteslist :
		#Il faut délimiter la vraie quote
		pos1=0
		pos2=0
		if (site==0):
			pos1=quote.find(">")+1
			pos2=quote.find("&lt;br /&gt;&lt;br /&gt;&lt;")
		if (site==1):
			pos1=quote.find(">")+1
			pos2=quote.find("&lt;br /&gt;&lt;br /&gt;&lt;")
		if (site==2):
			pos1=quote.find(">")+1
			pos2=quote.find("&lt")
		stmp=quote[pos1:pos2]
		#Ensuite la conversion, avec un cas spécial pour PEBKAC
		if (site==1):
			stmp=(stmp.encode("iso8859-1")).decode("utf-8")
			stmp=conversionHTML(stmp)
		else:
			stmp=conversionHTML(stmp)
		listoutput.append(stmp)
		
	return listoutput
		
