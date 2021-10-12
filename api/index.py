from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
import json
import urllib.request

def scrape_menu_to_str(url):
    soup = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    menudiv = soup.find("div", {"class": "menu__details"})
    category = menudiv.find_all("div",{"class": "station-header-title"})
    #print(category)

    k = dict()
    k['restaurant'] = []
    for x in range(len(category)):
        n = dict()
        n['category'] = category[x].string
        n['menu'] = []

        menu_cat = soup.find_all("div", {"class": "menu__station"})
        cat_list = menu_cat[x].find_all("li", {"class": "menu__item item"})
        #menu_name = menu_cat[x].find_all("a", {"class": "viewItem"})
        # print(menu_name)
        #calories = menu_cat[x].find_all("span", {"class": "item__calories"})
        # print(calories)
        #des = menu_cat[x].find_all("p", {"class": "item__content"})

        for y in range(len(cat_list)):
            z = dict()
            menu_name = cat_list[y].find("a", {"class": "viewItem"})
            calories = cat_list[y].find("span", {"class": "item__calories"})
            des = cat_list[y].find("p", {"class": "item__content"})
            vegan = cat_list[y]['isvegan']
            vegetarian = cat_list[y]['isvegetarian']
            eatwell = cat_list[y].find("ul", {"class": "unstyled item__allergens allergenList"})
            #print(eatwell)

            if menu_name != None:
                z["name"] = menu_name.string
            else:
                z["name"] = cat_list[y].find("span", {"class": "item__name"}).string

            if calories != None:
                z["calories"] = int(calories.string.split()[0])
            else:
                z["calories"] = 0

            if des != None:
                z["description"] = des.string
            elif des == None:
                z["description"] = 'N/A'

            z["isVegan"] = vegan

            z["isVegetarian"] = vegetarian

            z["isEatWell"] = False
            if eatwell!= None:
                for x in eatwell.find_all("img"):
                    #print(x)
                    if x["src"] == "/-/media/Global/All Divisions/Dietary Information/EatWell-80x80.png":
                        z["isEatWell"] = True

            z["isPlantForward"] = False
            if eatwell!= None:
                for x in eatwell.find_all("img"):
                    if x["src"] == "/-/media/Global/All Divisions/Dietary Information/PlantForward.png":
                        z["isPlantForward"] = True

            z["isWholeGrains"] = False
            if eatwell != None:
                for x in eatwell.find_all("img"):
                    if x["src"] == "/-/media/Global/All Divisions/Dietary Information/WholeGrains-80x80.png":
                        z["isWholeGrains"] = True


            n['menu'].append(z)

        k['restaurant'].append(n)
    return json.dumps(k)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        eatery_url = "https://uci.campusdish.com/en/LocationsAndMenus/TheAnteatery"
        brandy_url = "https://uci.campusdish.com/LocationsAndMenus/Brandywine"
        data = ""
        if "anteatery" in self.path:
            data = scrape_menu_to_str(eatery_url)
        elif "brandywine" in self.path:
            data = scrape_menu_to_str(brandy_url)
        else:
            self.send_response(404)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write("Invalid path. Needs to be /anteatery or /brandywine".encode())
            return
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(data.encode())
        return

