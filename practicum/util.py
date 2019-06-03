import urllib.request
import requests
from bs4 import BeautifulSoup, SoupStrainer
import json
import csv

# list of plants I have in my garden, easier to scrape plant information from burpee.com than to manually enter it all
url_list = [# herbs
            "https://www.burpee.com/herbs/basil/basil-genovese-prod000452.html",
            "https://www.burpee.com/herbs/chive/chives-prod000467.html",
            "https://www.burpee.com/herbs/cilantro/cilantro-calypso--prod001758.html",
            "https://www.burpee.com/herbs/dill/dill-mammoth-prod000472.html",
            "https://www.burpee.com/herbs/fennel/fennel-florence-prod000473.html",
            "https://www.burpee.com/perennials/lavenders/lavender-lady-prod000070.html",
            "https://www.burpee.com/herbs/oregano/oregano-greek-prod000480.html",
            "https://www.burpee.com/herbs/parsley/parsley-single-italian-prod000482.html",
            "https://www.burpee.com/herbs/rosemary/rosemary-arp-prod099728.html",
            "https://www.burpee.com/herbs/sage/sage-common-prod000484.html",
            "https://www.burpee.com/herbs/tarragon-mexican-22738.html",
            "https://www.burpee.com/herbs/thyme/thyme-common-prod000487.html",
            "https://www.burpee.com/herbs/verbena/verbena-lemon-24539.html",
            # vegetables
            "https://www.burpee.com/vegetables/arugula/arugula-rocket-roquette-prod000886.html",
            "https://www.burpee.com/vegetables/beans/bean-pole-fortex-prod000583.html",
            "https://www.burpee.com/vegetables/beets/beet-detroit-dark-red-medium-top-prod000611.html",
            "https://www.burpee.com/vegetables/broccoli/broccoli-sun-king-hybrid-prod003176.html",
            "https://www.burpee.com/vegetables/brussels-sprouts/brussels-sprouts-octia-hybrid-prod003199.html",
            "https://www.burpee.com/vegetables/cabbages/chinese-cabbage-pak-choi-toy-choi-hybrid-prod000626.html",
            "https://www.burpee.com/vegetables/cabbages/cabbage-early-jersey-wakefield-prod002049.html",
            "https://www.burpee.com/vegetables/carrots/carrot-touchon-prod000644.html",
            "https://www.burpee.com/vegetables/celery/celery-tall-utah-52-70r-improved-prod000649.html",
            "https://www.burpee.com/vegetables/corn/corn-ambrosia-hybrid-prod001817.html",
            "https://www.burpee.com/vegetables/cucumbers/cucumber-supremo-hybrid-prod003169.html",
            "https://www.burpee.com/vegetables/cucumbers/cucumber-sugar-crunch-hybrid-prod000701.html",
            "https://www.burpee.com/vegetables/eggplants/eggplant-early-midnight-hybrid-prod002717.html"
            "https://www.burpee.com/vegetables/eggplants/eggplant-millionaire-hybrid-prod000711.html",
            "https://www.burpee.com/vegetables/garlic/garlic-extra-select--prod000716.html",
            "https://www.burpee.com/vegetables/horseradish/horseradish-maliner-kren-69039.html",
            "https://www.burpee.com/vegetables/kale/kale-red-winter-organic-prod002231.html",
            "https://www.burpee.com/vegetables/leeks/leek-dawn-giant-prod001127.html",
            "https://www.burpee.com/vegetables/lettuce/lettuce-looseleaf-blend-prod000750.html",
            "https://www.burpee.com/vegetables/melon/cantaloupe-burpees-ambrosia-hybrid-prod000541.html",
            "https://www.burpee.com/vegetables/mesclun/mesclun-classic-mix-prod000759.html",
            "https://www.burpee.com/vegetables/okra/okra-clemson-spineless-prod000768.html",
            "https://www.burpee.com/vegetables/onions/bunching-onion-evergreen-long-white-organic-prod000774.html",
            "https://www.burpee.com/vegetables/onions/onion-collection-sets-prod000770.html",
            "https://www.burpee.com/vegetables/onions/onion-walla-walla-sweet-prod000779.html",
            "https://www.burpee.com/vegetables/parsnips/parsnip-hollow-crown-50336A.html",
            "https://www.burpee.com/vegetables/peas/pea-easy-peasy-prod002731.html",
            "https://www.burpee.com/vegetables/peas/pea-sugar-snap-prod000793.html",
            "https://www.burpee.com/vegetables/peppers/pepper-hot-big-guy-hybrid-prod002733.html",
            "https://www.burpee.com/vegetables/peppers/pepper-hot-habanero-prod000805.html",
            "https://www.burpee.com/vegetables/peppers/pepper-hot-pepperoncini-greek--prod099712.html",
            "https://www.burpee.com/vegetables/peppers/pepper-hot-serrano-chili-prod000819.html",
            "https://www.burpee.com/vegetables/peppers/pepper-sweet-california-wonder-prod000825.html",
            "https://www.burpee.com/vegetables/pumpkins/pumpkin-small-sugar-prod000867.html",
            "https://www.burpee.com/vegetables/radish/radish-perfecto-prod000878.html",
            "https://www.burpee.com/vegetables/spinach/spinach-babys-leaf-hybrid-prod000893.html",
            "https://www.burpee.com/vegetables/squash/squash-burpees-best-hybrid-prod003504.html"
            "https://www.burpee.com/vegetables/squash/squash-summer-golden-egg-hybrid-prod002741.html",
            "https://www.burpee.com/vegetables/squash/squash-winter-burpees-butterbush-prod000932.html",
            "https://www.burpee.com/vegetables/swiss-chard/swiss-chard-bright-lights-prod000947.html",
            "https://www.burpee.com/vegetables/tomatoes/tomato-big-mama-hybrid-prod000966.html",
            "https://www.burpee.com/vegetables/tomatoes/tomato-brandy-boy--hybrid-prod000973.html",
            "https://www.burpee.com/vegetables/tomatoes/tomato-cherry-baby-hybrid-prod099561.html",
            "https://www.burpee.com/vegetables/turnips/turnip-purple-top-white-globe-prod001185.html",
            # fruits
            "https://www.burpee.com/fruit/watermelon/watermelon-georgia-rattlesnake-prod000557.html",
            "https://www.burpee.com/fruit/honeydew/honeydew-dolce-nectar-hybrid-prod003510.html",
            # flowers
            "https://www.burpee.com/flowers/calendula/calendula-pacific-beauty-mix-organic-49405A.html"]

def fetch_data():
    plants = {}
    for url in url_list:
        resp = urllib.request.urlopen(url)
        soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
        plant_properties = {}
        name = soup.find('h1', class_ = "b-product_name")
        name = name.get_text().strip()
        for prop in soup.find_all('div', class_ = "b-product_properties-item"):
            p_name = prop.find('span', class_="js-product-properties-name")
            p_value = prop.find('p', class_="b-product_properties-property_value")
            plant_properties[p_name.get_text()] = p_value.get_text().strip()
        for prop in soup.find_all('div', class_ = "b-product_attribute"):
            p_name = prop.find('div', class_="b-product_attribute-title")
            if p_name.get_text().strip() not in plant_properties:
                p_value = prop.find('div', class_="b-product_attribute-description")
                plant_properties[p_name.get_text().strip()] = p_value.get_text().strip()
            
        plants[name] = plant_properties
    with open("plants.json", "a") as out_file:
        out_file.write(json.dumps(plants))

    for k,v in plants.items():
        print(k, v,'\n')

def get_common_name(plant_name):
    plant_name = plant_name.lower()
    alliums = [ "scallion", "shallot"]
    if any(name in plant_name for name in alliums):
        return "Alliums"
    if "bean" in plant_name and "pole" in plant_name:
        return "Beans, pole"
    if "beets" in plant_name:
        return "Beets"
    brassicas = ["kale","choy"]
    if any(name in plant_name for name in brassicas):
        return "Brassicas"
    if "broccoli" in plant_name:
        return "Broccoli"
    if "brussels" in plant_name:
        return "Brussels sprouts"
    if "cabbage" in plant_name:
        return "Cabbage"
    if "carrot" in plant_name:
        return "Carrots"
    if "cauliflower" in plant_name:
        return "Cauliflower"
    if "celery" in plant_name:
        return "Celery"
    if "chard" in plant_name:
        return "Chard"
    if "corn" in plant_name:
        return "Corn / Maize"
    if "cucumber" in plant_name:
        return "Cucumber"
    if "eggplant" in plant_name:
        return "Eggplant or Aubergine"
    if "leek" in plant_name:
        return "Leek"
    if "lettuce" in plant_name:
        return "Lettuce"
    if "okra" in plant_name:
        return "Okra"
    if "onion" in plant_name:
        return "Onion"
    if "parsnip" in plant_name:
        return "Parsnip"
    if "peas" in plant_name:
        return "Peas"
    if "pepper" in plant_name:
        return "Peppers"
    if "pumpkin" in plant_name:
        return "Pumpkin"
    if "radish" in plant_name:
        return "Radish"
    if "spinach" in plant_name:
        return "Spinach"
    if "squash" in plant_name:
        return "Squash"
    if "tomato" in plant_name:
        return "Tomatoes"
    if "turnip" in plant_name or "rutabaga" in plant_name:
        return "Turnips and rutabagas"
    if "basil" in plant_name:
        return "Basil"
    if "chive" in plant_name:
        return "chive"
    if "cilantro" in plant_name or "coriander" in plant_name:
        return "Cilantro / Coriander"
    if "dill" in plant_name:
        return "Dill"
    if "fennel" in plant_name:
        return "Fennel"
    if "garlic" in plant_name:
        return "Garlic"
    if "lavender" in plant_name:
        return "Lavender"
    if "oregano" in plant_name:
        return "Oregano"
    if "parsley" in plant_name:
        return "Parsley"
    if "rosemary" in plant_name:
        return "Rosemary"
    if "sage" in plant_name:
        return "Sage"
    if "tarragon" in plant_name:
        return "Tarragon"
    if "thyme" in plant_name:
        return "Thyme"
    if "calendula" in plant_name or "marigold" in plant_name:
        return "Marigold"


