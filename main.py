from os import error, mkdir
import os
from selenium import webdriver
import requests

chrome_web_driver_path = "C:\Chrome_Driver\chromedriver.exe"
already_downloaded = []
wallpaper_urls = []
count = 1

def check_url(url):
    print(url)
    if len(url.strip()) == 0:
        print("You haven't entered any url!")
        return False
    else:
        r = requests.get(url)
        if r.status_code == 200:
            print(f"Status code {r.status_code}: Connection Successful!")
            return True
        else:
            print(f"Status code {r.status_code}: There's an err.. search the status code.. aborting..")
            return False

def retrieve_downloaded():
    global already_downloaded
    # print(url)
    try:
        with open("downloaded_wallpapers.txt") as d:
            content = d.readlines()
            already_downloaded = [item.replace("\n", "") for item in content]
        print(already_downloaded)
    except error:
        print(error)

def num_of_images(url,page_num):
    global wallpaper_urls
    wallpaper_urls = []
    print(f"\n\n\nNum of images: {url}\n\n\n")
    driver = webdriver.Chrome(executable_path=chrome_web_driver_path)
    print(f"\n\nOpening page: {page_num}... \n\n")
    driver.get(url)
    previews_links = []
    previews_links = driver.find_elements_by_xpath('//*[@id="thumbs"]/section[1]/ul/li/figure/a')
    print(f"\n\n\t\t\t***** There are {len(previews_links)} images on page {page_num} *****");
    previews_links2 = []
    previews_links2 = [item.get_attribute("href").split("/")[-1] for item in previews_links]
    # print(previews_links2)
    wallpaper_urls = [f"https://w.wallhaven.cc/full/{item[:2]}/wallhaven-{item}.jpg" for item in previews_links2]
    # print(wallpaper_urls);
    driver.quit()


def download_wallpaper(u):
    global count
    # print(url)
    if not os.path.isdir("wallpapers"):
        print("Creating wallpapers directory..")
        mkdir("wallpapers")
    if u in already_downloaded:
        print(f"Wallpaper at {u} already exists!")
    else:
        r = requests.get(u)
        if r.status_code == 200:
            with open(f"wallpapers/{u.split('-')[-1]}", "wb") as wallpaper:
                print(f"Downloading image {count} from url: {u}")
                wallpaper.write(r.content)
                count +=1
                print("Downloaded Successfully!")
            with open("downloaded_wallpapers.txt", "a") as d:
                d.write(f"{u}\n")
        else:
            print(f"Status code {r.status_code}.Error downloading image {count} at url: {u}")
            count += 1

def download_maybe(url):
    global count
    
    driver = webdriver.Chrome(executable_path=chrome_web_driver_path)
    for _ in range(1, NUM_OF_PAGES + 1):
        count = 1
        page_url = f"{url}page={_}"
        num_of_images(page_url,page_num=_)
        for u in wallpaper_urls:
            # print(url)
            driver.get(u)
            d = input(f"Download this wallpaper( url: {u} ) (Y/n)?: ")
            print(f"\n\n\nuser choice: {d}\n\n\n")
            if len(d.strip()) == 0 or d.lower() == "y":
                download_wallpaper(u)
            else:
                print("Ok.. not downloading this one.. moving on!")
                count += 1

def download_all(url):
    global count
    for _ in range(1, NUM_OF_PAGES + 1):
        count = 1
        page_url = f"{url}page={_}"
        num_of_images(page_url,page_num=_)
        for u in wallpaper_urls:
            # print(url)
            download_wallpaper(u)


ALPHA_URL = input("Enter url:")
if check_url(ALPHA_URL):
    if "page" in ALPHA_URL:
        print("has page in it")
        url = ALPHA_URL.split("page")[:1][0]
    else:
        print("doesn't have page in it")
        url = ALPHA_URL
    NUM_OF_PAGES = int(input("Enter num of pages:"))
    all_or_s = input("Download all at once? (Y/n)?:")
    retrieve_downloaded()
    if len(all_or_s.strip()) == 0 or all_or_s.lower() == "y":
        download_all(url)
    else:
        download_maybe(url)