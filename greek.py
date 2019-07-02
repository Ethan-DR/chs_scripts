# -*- coding: utf-8 -*-
import sys
import unicodedata
import xml.etree.ElementTree as ET
import unittest

def main():
	EngInfo = []
	GrcInfo = []
	notelang = ""
	index = 0
	for file in sys.argv[1:]:
		tree = ET.parse("/users/intern4/desktop/perseus_files_to_be_added/" + file)
		root = tree.getroot()
		TEI = "{http://www.tei-c.org/ns/1.0}"
		for header in tree.iter("teiHeader"):
			print(header.find("fileDesc").find("titleStmt").find("title").text)
		# this is to check if we only have a bunch of div1's see file 080
		# if so it reformats to the "standard" we expect for an un edited file
		print(root.find("text").find("body").find("div1").findall("div2"))
		if root.find("text").find("body").find("div1").findall("div2") == []:
			for d in root.find("text").find("body").findall("div1"):
				d.tag = "div2"
			d1 = ET.Element("div1")
			d1.set("type","chapter")
			root.find("text").find("body").insert(1, d1)
			rank = 1
			# moves milestone to inside overarching div
			milestone = root.find("text").find("body").find("milestone")
			# if there are milestone issues revert this condition to just if milestone:
			if milestone is not None:
				root.find("text").find("body").find("div1").insert(0, milestone)
				root.find("text").find("body").remove(milestone)
			# moves secondary divs into overarching div
			for d2 in root.find("text").find("body").findall("div2"):
				root.find("text").find("body").find("div1").insert(rank, d2)
				root.find("text").find("body").remove(d2)
				rank += 1
		for x in tree.iter():
			# changing TEI.2
			if x.tag == "TEI.2":
				x.tag = "TEI"
				x.set("xmlns","http://www.tei-c.org/ns/1.0")
			
			# changing teiHeader
			if x.tag == "teiHeader":
				x.set("xml:lang","eng")

			# MUST CHANGE THE TITLE MANUALLY AND

			# removes <title type="sub">Machine readable text</title>
			# determines editor and therefore if to tag notes as lat or eng
			if x.tag == "titleStmt":
				for element in x.iter():
					if element.text == "Machine readable text":
						x.remove(element)
					if element.tag == "editor":
						if element.text[-11:] == "Bernardakis":
							notelang = "lat"
							# u is to make sure the string is unicode. Changes Bernardakis to the correct spelling
							element.text = u"Grēgorios N. Vernardakēs"
						if element.text[-7:] == "Babbitt":
							notelang = "eng"

			# removing n from author
			if x.tag == "author":
				print("found author")
				print(x.attrib)
				if x.attrib:
					print("test")
					del x.attrib["n"]


			# changing names
			if x.tag == "respStmt":
				for y in x.findall("name"):
					if y.text == "William Merrill":
						y.text = "Rashmi Singhal"
					if y.text == "Elli Mylonas":
						y.text = "Bridget Almas"
					if y.text == "David Smith":
						x.remove(y)

			# removing extent
			if x.tag == "fileDesc":
				extent = x.find("extent")
				x.remove(extent)

			# removing analytic
			if x.tag == "biblStruct":
				analytic = x.find("analytic")
				x.remove(analytic)
				if x.find("monogr").find("editor").text[-11:] == "Bernardakis":
					# u is to make sure the string is unicode. Changes Bernardakis to the correct spelling
					x.find("monogr").find("editor").text = u"Grēgorios N. Vernardakēs"


			# adding release date
			if x.tag == "publicationStmt":
				date = ET.SubElement(x, "date")
				date.set("type", "release")
				date.text = "2010-12-13"
			
			# MUST CHECK DATE OF PUB INFO YOURSELF

			# updating biblScope attribute
			if x.tag == "biblScope":
				if x.attrib:
					del x.attrib["type"]
				x.set("unit","volume")

			# adding ref to end of biblStruct
			# MUST ADD URL YOURSELF
			if x.tag == "biblStruct":
				ref = ET.SubElement(x, "ref")
				ref.set("target", "URL HERE")
				ref.text = "The Internet Archive"

			# adding <p> between editorialDecl and refsDecl
			if x.tag == "encodingDesc":
				p1 = ET.Element("p")
				p1.text = "Text encoded in accordance with the latest EpiDoc standards"
				x.insert(1, p1)
				p2 = ET.Element("p")
				p2.text = "The following text is encoded in accordance with EpiDoc standards and with the CTS/CITE Architecture"
				x.insert(2, p2)

				# updating refsDecl tags:
				refsDecl = x.find("refsDecl")
				if refsDecl.attrib:
					del refsDecl.attrib["doctype"]
				refsDecl.set("n","CTS")

				# adding correct cRefPattern and p
				cRefPattern = ET.SubElement(refsDecl,"cRefPattern")
				cRefPattern.set("n","section")
				cRefPattern.set("matchPattern","(\\w+)")
				cRefPattern.set("replacementPattern","#xpath(/tei:TEI/tei:text/tei:body/tei:div/tei:div[@n='$1'])")
				cRefPatternP = ET.SubElement(cRefPattern,"p")
				cRefPatternP.text = "This pointer pattern extracts sections"


			# MUST CHANGE STATE STUFF MANUALLY

			# changing langage id
			if x.tag == "language":
				idtext = x.attrib["id"]
				if idtext == "greek":
					idtext = "grc"
				if idtext == "latin":
					idtext == "lat"
				if idtext == "english":
					idtext == "eng"
				if idtext == "german":
					idtext = "deu"
				del x.attrib["id"]
				x.set("ident", idtext)

			# MUST CHANGE RESP STUFF MANUALLY BOTH CHANGE AND ADD

			# changing id to xml:id
			if x.attrib:
				try:
					idtext = x.attrib["id"]
					del x.attrib["id"]
					x.set("xml:id", idtext)
				except:
					# seem to need something here for this to work
					a = 1

			# TEXT STUFF NOW
			# changing lang tag in overarching text element
			if x.tag == "text":
				x.set("xml:lang","grc")
				
			# gets the pb info that we need to rewrite pb under the initial div, also rewrite the pb
			# this may cause pb rewriting problems if there is more than one body	
			if x.tag == "body":
				pb = x.find("pb")
				pba = pb.attrib["id"]
				x.remove(pb)
				x.find("div1")
				pb1 = ET.Element("pb")
				pb1.set("xml:id",pba)
				x.insert(0,pb1)

			# getting div1 to div adding attributes
			# MUST MANUALLY DO MILESTONE. IF PREFER TO JUST DO THE <> THEN UNCOMMENT BELOW
			if x.tag == "div1":
				x.tag = "div"
				if "n" in x.attrib:
					x.set("type", "textpart")
					x.set("subtype", "chapter")
				else:
					x.set("type","edition")
					x.set("n","urn:cts:greekLit:" + file[:-4])
				x.set("xml:lang","grc")
				# q = x.find("div2").find("milestone")
				# initialp = x.find("div2").find("p")
				# initialp.text = "<milestone unit=\"".encode('utf-8') + q.attrib["unit"] + "\" id=\"" + q.attrib["id"] + "\" n=\"" + q.attrib["n"] + "\"/> " + initialp.text
				# del q.tag

			# getting div2 attribute and adding indent to first p tag
			if x.tag == "div2":
				x.tag = "div"
				x.set("subtype", "section")
				x.set("type", "textpart")
				x.find("p").set("rend", "indent")
				
				
			# changing lang to xml:lang
			if x.attrib: 
				try:
					lang = x.attrib["lang"]
					if lang == "greek":
						lang = "grc"
					if lang == "latin":
						lang == "lat"
					if lang == "english":
						lang == "eng"
					if lang == "german":
						lang = "deu"
					del x.attrib["lang"]
					x.set("xml:lang",lang)
				except:
					a=1

			# changing notes
			if x.tag == "note":
				x.set("anchored","true")
				if notelang != "":
					x.set("xml:lang", notelang)

			# changing gap
			if x.tag == "gap":
				x.set("reason","lost")

			# changing q
			if x.tag =="q":
				x.set("type","unspecified")
				del x.attrib["direct"]

			# MUST CHANGE SINGLE AND DOUBLE QUOTES

	tree.write(file[:-5] + str(int(file[-5]) + 1) +".xml" , encoding="UTF-8",xml_declaration=True)
	print("done")
if __name__ == '__main__':
    main()


