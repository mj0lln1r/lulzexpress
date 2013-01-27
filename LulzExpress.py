#!/usr/bin/python3

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


from tkinter import *
from LulzParser import *

class Reader(object):
  """ Classe qui contient l'application : les boutons radios, la zone texte et les boutons """
	def __init__(self,master):
		""" Instanciation des widgets et des attributs de la classe Reader() """
		#Choix du site à lire
		self.choice=IntVar()
		self.choice.set(-1)
		#Listes d'indentification des sites DTC=0,PBK=1,VDM=2
		self.site=["DTC","PBK","VDM"]
		self.url=["http://feeds.feedburner.com/bashfr-quotes?format=xml","http://feeds.feedburner.com/Pebkacfr?format=xml","http://feeds.feedburner.com/viedemerde?format=xml"]
		#Nombre max de lignes suivant le site à lire
		self.lines=30
		#Maximum de quotes chargées
		self.maximum=0
		#Minimum de quotes
		self.minimum=0
		#Position de lecture actuelle
		self.pos=0
		#Liste des quotes chargées
		self.quotes=[]
		#Série des boutons radios à créer
		self.rdDTC=Radiobutton(master,text="DTC",variable=self.choice,value=0,command=self.handler)
		self.rdPBK=Radiobutton(master,text="Pebkac",variable=self.choice,value=1,command=self.handler)
		self.rdVDM=Radiobutton(master,text="VDM",variable=self.choice,value=2,command=self.handler)
		#Zone Texte où s'afficheront les quotes
		self.quotezone=Text(master, width=80,height=self.lines,wrap=WORD,relief=GROOVE)
		#Boutons de commande
		self.prevb=Button(text="Previous",command=self.printprev)
		self.nextb=Button(text="Next",command=self.printnext)
		self.quitb=Button(text="Quit",command=master.destroy)
		#Mise en grille des widgets
		self.rdDTC.grid(row=0, column=1)
		self.rdPBK.grid(row=0, column=3)
		self.rdVDM.grid(row=0, column=5)
		self.quotezone.grid(row=1, column=0, columnspan=7)
		self.prevb.grid(row=2,column=1)
		self.nextb.grid(row=2,column=3)
		self.quitb.grid(row=2,column=5)
	
	def handler(self):
		""" Méthode qui va charger les quotes suivant le choix de l'user """
		#Récupération du fil RSS sous forme XML
		xmlfile=xmldownload(self.url[self.choice.get()],self.site[self.choice.get()])
		#Parsing et traitement du fichier XML : chaque site aura son propre traitement
		self.quotes=parser(xmlfile,self.choice.get())
		#Initialisation des positions min,max et current
		self.maximum=len(self.quotes)
		if(self.choice.get()!=2):
			self.minimum=1
		self.pos=self.minimum
		#Affichage de la première quote
		self.printquote()
	
	def printquote(self):
		""" Méthode qui s'occupe d'afficher la quote dans la zone texte """
		self.quotezone.delete(1.0,END)
		self.quotezone.insert(END,self.quotes[self.pos])	
	
			
	def printprev(self):
		""" Méthode qui affiche la quote précedente sous condition """
		if (self.pos-1>0):
			self.pos-=1
			self.printquote()
			
	def printnext(self):
		""" Méthode qui affiche la quote suivante sous condition """ 
		if (self.pos+1<self.maximum):
			self.pos+=1
			self.printquote()
		
master=Tk()
master.title("Lulz Express")
reader=Reader(master)
master.mainloop()
