from bs4 import BeautifulSoup
import requests
import re
import os
from fpdf import FPDF
from PIL import Image

url = "https://toonily.net/manga/overgeared/chapter-89/"

source = requests.get(url).text

soup = BeautifulSoup(source , 'lxml')

imagesList = []

#print(soup.findAll('div'))

for link in soup.findAll('img' , attrs={"class":"wp-manga-chapter-img"}):
    imagesList.append(link['src'])

#print(images[17])
# https://stackoverflow.com/questions/37807568/get-only-the-image-filename-from-a-url-with-regex/37807634

#    [\w-]+\.png

imageNames = []

# print(imagesList)

for x in imagesList:
	imageNames.append(re.findall(r"[\w-]+\.jpg", x))

#print(imageNames[1])	

mangaName = re.findall(r"manga/([\w\-\.]+)", url)
chapterNum = re.findall(r"(chap[\w\-\.]+)", url)

root_directory = os.getcwd()
path = mangaName[0] + "/" +chapterNum[0]
os.makedirs(path)

i=0
for it in imagesList :
	if i > 9 :
		prefix = "C1"
	else:
		prefix = "C0"
	final_name = os.path.join(root_directory, mangaName[0], chapterNum[0], prefix +  imageNames[i][0]) 
	response = requests.get(it)
	f= open(final_name,'wb')
	f.write(response.content)
	f.close()

	i=i+1
    
path2 = os.path.join(root_directory, mangaName[0], chapterNum[0])
im_paths = os.listdir(path2)

pdf = FPDF()

for image in im_paths:
    cover = Image.open(os.path.join(path2, image))
    width, height = cover.size

    # convert pixel in mm with 1px=0.264583 mm
    width, height = float(width * 0.264583), float(height * 0.264583)

    # given we are working with A4 format size 
    pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

    # get page orientation from image size 
    orientation = 'P' if width < height else 'L'

    #  make sure image size is not greater than the pdf format size
    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

    pdf.add_page(orientation=orientation)
    pdf.image(path2 + "/" + image,100,0,0, height) # for A4 size because some people said that every other page is blank
pdf.output(chapterNum[0] + ".pdf", "F")