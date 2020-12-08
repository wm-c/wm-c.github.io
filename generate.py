import re
import os
from typing import List, Optional, Dict


def readMeta(file: str) -> Dict[str,str]:
	with open(file, "r") as meta:
		newLine = meta.readline()
		if(re.search("/\*", newLine) != None):
			newLine = meta.readline()
			metaDict = {}

			while(re.search("\*/", newLine) == None):
				newLine = newLine.replace("\n", "").split(":")

				metaDict[newLine[0]] = newLine[1]

				newLine = meta.readline()

			if(metaDict.get("fileGenerationSpot", None) == None):
				title = metaDict.get("Title", "noTitle")
				metaDict["fileGenerationSpot"] = f"generatedPosts/{title.replace(' ', '')}.html"
				

			return metaDict


	return None


def addPost(file: str, title: str, description: str, fileGenerationSpot: Optional[str] = None) -> None:
	if not fileGenerationSpot:
		fileGenerationSpot = f"generatedPosts/{title.replace(' ', '')}.html"
	

	with open(file, "a") as posts:
		posts.write(f"{title}:: {description}:: {fileGenerationSpot}\n")

# fix multi line bug
def styleText(stylableText: str) -> str:
	stylable = re.findall("\[(.*)\}", stylableText)

	
	for customStyle in stylable:

		splitPosition = customStyle.find("]")

		styledText = f'<span style="{customStyle[splitPosition + 2:]}">{customStyle[:splitPosition]}</span>'
		

		stylableText = stylableText.replace("[" + customStyle + "}", styledText)


	return stylableText


def getHeader(pageData: List[str]) -> str:
	header = ""

	try:
		headerLine = pageData.index("Header:\n")
	except ValueError as identifier:
		print("WARNING no header found")
		return header

	for line in pageData[headerLine+1:]:
		if(line == "\n"):
			return "<h1>" + styleText(header) + "</h1>"

		header += str(line).replace("\n", "")
	

def getText(pageData: List[str]) -> str:
	text = ""
	end = 0

	try:
		textLine = pageData.index("Text:\n")
	except ValueError as identifier:
		print("WARNING no text found")
		return text

	for line in pageData[textLine+1:]:
		if(line == "\n"):
			end += 1
			if(end == 3):
				return "<p>" + styleText(text) + "</p>"

		text += line

	return "<p>" + styleText(text) + "</p>"


def generatePage(file: str, generationPath: str, title: str) -> None:
	
	inHeader = False
	rawPost = open(file, "r")
	
	post = rawPost.readlines()

	header = getHeader(post)
	text = getText(post)

	with open("pages/template.html", "r") as template:
		lines = template.readlines()

		startAt = lines.index("	<!-- Add Title Here -->\n")
		lines[startAt] = f"<title>{title}</title>\n"

		startAt = lines.index("	<!-- Inject Text Here -->\n")

		lines[startAt+2] = header + "\n"
		lines[startAt+3] = text

	with open(generationPath, "w") as newPost:
		for line in lines:
			newPost.write(line)

	rawPost.close()
 
def writeAtomHeader(filename: str, baseurl: str, title: str, author: str) -> None:
    with open(filename, "w") as fp:
        fp.write(
			f"""
<?xml version="1.0" encoding="UTF-8"?>
<feed xml:lang="en-US"
    xmlns="http://www.w3.org/2005/Atom"
    xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
    <id>{baseurl}/feed.xml</id>
    <link rel="alternate" type="text/html" href="{baseurl}"/>
    <link rel="self" type="application/atom+xml" href="{baseurl}/feed.xml"/>
    <title>{title}</title>
    <author>
        <name>{author}</name>
    </author>
"""
		)
        
def writeAtomFooter(filename: str) -> None:
    with open(filename, "a") as fp:
        fp.write(
			f"""
</feed>
"""
		)
        
def writeFeedItem(filename: str, url: str, title: str, date: str, body: str) -> None:
    with open(filename, "a") as fp:
        fp.write(
			f"""
<entry>
	<id>{url}</id>
	<published>{date}</published>
	<link rel="alternate" type="text/html" href="{url}"/>
	<title>{title}</title>
	<content type="html">
		{body}
	</content>
</entry>
"""
		)

def main() -> int:

	posts = os.listdir("posts")
 
	if len(posts) == 0:
		print("No posts found")
		return 1

	# Write an ATOM feed header
	writeAtomHeader("feed.xml", "https://wm-c.dev", "WM-C", "William Meathrel")

	for post in posts:
		# Resets posts
		posts = open("Posts.txt", "w")
		posts.write("")
		posts.close()

		# gets path
		post = "posts/" + post

		# gets meta
		meta = readMeta(post)

		# adds and generates
		addPost("Posts.txt", meta.get("Title"), meta.get("Text"), meta.get("fileGenerationSpot"))
		generatePage(post, meta.get("fileGenerationSpot"), meta.get("Title", "No Title"))
		writeFeedItem("feed.xml", f"https://wm-c.dev", meta.get("Title"), meta.get("Date"), meta.get("Text"))
	
	return 0
	
if __name__ == "__main__":
	exit(main())