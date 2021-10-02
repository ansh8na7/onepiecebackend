# from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs4
from django.http import JsonResponse, HttpResponse


def scrapper(chapter):
    url = "https://myonepiecemanga.com/manga/one-piece-chapter-" + \
        str(chapter)+"/"
    r = requests.get(url)
    htmlContent = r.content
    soup = bs4(htmlContent, 'html.parser')
    # content = soup.find_all("div", {"class": "entry-content"})
    images = soup.find_all('img')
    count = 0
    imageList = []
    for image in images:
        img = dict()
        if image.has_attr('data-lazy-src'):
            if image.has_attr('class') and image['class'] != "SponsorAds":
                continue
            # print(image)
            # print("====================")
            img['id'] = count
            count += 1
            img['url'] = "https:" + image['data-lazy-src']
            if image.has_attr('height'):
                img['height'] = image["height"]
            if image.has_attr('width'):
                img["width"] = image["width"]
            imageList.append(img)
    return imageList


def index(request):
    return HttpResponse("<h2>This is a manga reader API for one piece english.</h2><h3>Add chapter no at the end of this url to get the chapter pages.</h3>")


def chapterView(request, chapter=2020):
    imageList = scrapper(chapter)

    return JsonResponse({"data": imageList})
