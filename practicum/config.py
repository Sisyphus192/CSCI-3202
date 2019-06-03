import datetime

# these were not used for anything, but I dont want to have to look them up again if use them for something in the future
# they are specific to Lakewood, CO
last_frost = datetime.date(2019, 5, 9)
no_frost = datetime.date(2019, 5, 24)

# the following are some preplanned beds from https://www.gardeners.com/kitchen-garden-planner/preplanned-gardens
# these beds do not initially satisfy our contraints, and are used as examples

preplanned_gardens = {
    "all american" : {
        "plants": {
            "Tomato, Big Mama Hybrid":3,
            "Pepper, Sweet, California Wonder":2,
            "Spinach, Baby's Leaf Hybrid": 2,
            "Bean, Pole, Fortex": 1,
            "Basil, Genovese": 1,
            "Broccoli, Sun King Hybrid":2,
            "Kale, Red Winter Organic":1,
            "Swiss Chard, Bright Lights":1,
            "Parsley, Single Italian":1,
            "Beet, Detroit Dark Red Medium Top":3,
            "Lettuce, Looseleaf Blend":1},
        "size": (3,6)},
    "cooks choice" : {
        "plants": {
            "Basil, Genovese":2,
            "Onion Collection, Sets":3,
            "Spinach, Baby's Leaf Hybrid":2,
            "Tomato, Big Mama Hybrid":3,
            "Parsley, Single Italian":1,
            "Pepper, Sweet, California Wonder":2,
            "Bean, Pole, Fortex":1,
            "Swiss Chard, Bright Lights":1,
            "Lettuce, Looseleaf Blend":3},
        "size": (3,6)},
    "giving garden" : { 
        "plants": {
            "Squash, Winter, Burpee's Butterbush":8,
            "Cabbage, Early Jersey Wakefield":4,
            "Kale, Red Winter Organic":4,
            "Swiss Chard, Bright Lights":4,
            "Carrot, Touchon":8,
            "Beet, Detroit Dark Red Medium Top":4},
        "size": (4,8)},
    "high yield" : {
        "plants": {
            "Squash, Winter, Burpee's Butterbush":1,
            "Eggplant, Millionaire Hybrid":1,
            "Tomato, Big Mama Hybrid":3,
            "Squash, Summer, Golden Egg Hybrid":1,
            "Cucumber, Supremo Hybrid":2,
            "Pepper, Sweet, California Wonder":2,
            "Swiss Chard, Bright Lights":1,
            "Kale, Red Winter Organic":1,
            "Basil, Genovese":1,
            "Bean, Pole, Fortex":2,
            "Beet, Detroit Dark Red Medium Top":2,
            "Parsley, Single Italian":1},
        "size": (3,6)},
    "salad garden" : {
        "plants": {
            "Tomato, Big Mama Hybrid":2,
            "Pepper, Sweet, California Wonder":1,
            "Kale, Red Winter Organic":2,
            "Cilantro, Calypso":2,
            "Bunching Onion, Evergreen Long White Organic":1,
            "Cucumber, Supremo Hybrid":2,
            "Swiss Chard, Bright Lights":1,
            "Lettuce, Looseleaf Blend":1,
            "Mesclun, Classic Mix":1,
            "Arugula, Rocket (Roquette)":1,
            "Lettuce, Looseleaf Blend":1,
            "Radish, Perfecto":1},
        "size": (2,8)},
    "fun for kids" : {
        "plants": {
            "Carrot, Touchon":2,
            "Pea, Easy Peasy":3,
            "Corn, Ambrosia Hybrid":3,
            "Honeydew, Dolce Nectar Hybrid":2,
            "Tomato, Big Mama Hybrid":2,
            "Bean, Pole, Fortex":2,
            "Calendula, Pacific Beauty Mix Organic":1,
            "Celery, Tall Utah 52-70R Improved":1,
            "Pumpkin, Small Sugar":1,
            "Cucumber, Supremo Hybrid":1},
        "size": (3,6)},
    "kitchen herb" : {
        "plants": {
            "Calendula, Pacific Beauty Mix Organic":2,
            "Basil, Genovese":4,
            "Oregano, Greek":1,
            "Chives":2,
            "Sage, Common":1,
            "Rosemary, Arp":1,
            "Thyme, Common":1,
            "Cilantro, Calypso":2,
            "Parsley, Single Italian":2,
            "Dill, Mammoth":2},
        "size": (2,8)},
    "mediterranean garden" : {
        "plants": {
            "Pepper, Hot, Pepperoncini Greek":1,
            "Pepper, Sweet, California Wonder":1,
            "Tomato, Big Mama Hybrid":2,
            "Eggplant, Millionaire Hybrid":2,
            "Squash, Summer, Golden Egg Hybrid":2,
            "Swiss Chard, Bright Lights":2,
            "Lettuce, Looseleaf Blend":1,
            "Mesclun, Classic Mix":1,
            "Bunching Onion, Evergreen Long White Organic":2,
            "Cucumber, Supremo Hybrid":2},
        "size": (2,8)},
    "plant it & forget it" : {
        "plants": {
            "Cucumber, Supremo Hybrid":2,
            "Onion Collection, Sets":3,
            "Pepper, Hot, Pepperoncini Greek":1,
            "Bean, Pole, Fortex":1,
            "Squash, Summer, Golden Egg Hybrid":1,
            "Pepper, Sweet, California Wonder":2,
            "Tomato, Big Mama Hybrid":2,
            "Squash, Winter, Burpee's Butterbush":1,
            "Beet, Detroit Dark Red Medium Top":2,
            "Carrot, Touchon":2,
            "Basil, Genovese":1},
        "size": (3,6)},
    "salad bar" : {
        "plants": {
            "Lettuce, Looseleaf Blend":1,
            "Pea, Easy Peasy":3,
            "Broccoli, Sun King Hybrid":2,
            "Tomato, Big Mama Hybrid":3,
            "Spinach, Baby's Leaf Hybrid":1,
            "Swiss Chard, Bright Lights":1,
            "Pepper, Sweet, California Wonder":2,
            "Eggplant, Millionaire Hybrid":1,
            "Lettuce, Looseleaf Blend":1,
            "Cucumber, Supremo Hybrid":2,
            "Basil, Genovese":1},
        "size": (3,6)},
    "salsa & tomato sauce" : {
        "plants": {
            "Parsley, Single Italian":1,
            "Onion Collection, Sets":4,
            "Pepper, Hot, Pepperoncini Greek":2,
            "Cilantro, Calypso":2,
            "Tomato, Big Mama Hybrid":5,
            "Basil, Genovese":2,
            "Pepper, Sweet, California Wonder":2},
        "size": (3,6)},
    "salsa garden" : {
        "plants": { 
            "Tomato, Big Mama Hybrid":3,
            "Pepper, Sweet, California Wonder":2,
            "Pepper, Hot, Pepperoncini Greek":2,
            "Basil, Genovese":1,
            "Onion Collection, Sets":2,
            "Bunching Onion, Evergreen Long White Organic":2,
            "Cilantro, Calypso":3,
            "Parsley, Single Italian":1},
        "size": (2,8)},
    "stir fry garden" : {
        "plants": {
            "Eggplant, Millionaire Hybrid":1,
            "Pepper, Sweet, California Wonder":2,
            "Broccoli, Sun King Hybrid":2,
            "Kale, Red Winter Organic":1,
            "Squash, Summer, Golden Egg Hybrid":2,
            "Bean, Pole, Fortex":2,
            "Carrot, Touchon":2,
            "Chinese Cabbage, Pak Choi, Toy Choi Hybrid":2,
            "Bunching Onion, Evergreen Long White Organic":2},
        "size": (2,8)}
}

# this was custom plant selection when debugging
num_plants = {"Tomato, Big Mama Hybrid": 3,
              "Pepper, Sweet, California Wonder": 2,
              "Spinach, Baby's Leaf Hybrid": 4,
              "Bean, Pole, Fortex": 1,
              "Basil, Genovese": 3,
              "Broccoli, Sun King Hybrid": 2,
              "Kale, Red Winter Organic": 1,
              "Swiss Chard, Bright Lights": 1,
              "Parsley, Single Italian": 1,
              "Beet, Detroit Dark Red Medium Top": 3,
              "Lettuce, Looseleaf Blend": 1,
              }

# total list off all plants Derek Thomas wants to plant
"""
num_plants = {"Tomato, Big Mama Hybrid": 3,
              "Tomato, Brandy Boy  Hybrid": 3,
              "Pepper, Sweet, California Wonder": 6,
              "Spinach, Baby's Leaf Hybrid": 2,
              "Bean, Pole, Fortex": 2,
              "Basil, Genovese": 4,
              "Broccoli, Sun King Hybrid": 2,
              "Kale, Red Winter Organic": 4,
              "Swiss Chard, Bright Lights": 4,
              "Parsley, Single Italian": 2,
              "Beet, Detroit Dark Red Medium Top": 4,
              #"Lettuce, Looseleaf Blend": 1,
              "Onion Collection, Sets": 2,
              "Onion, Walla Walla Sweet": 1,
              #"shallots": 1,
              "Lettuce, Looseleaf Blend": 3,
              "Squash, Winter, Burpee's Butterbush": 8,
              "Cabbage, Early Jersey Wakefield": 4,
              "Carrot, Touchon": 8,
              "Eggplant, Millionaire Hybrid": 2,
              "Squash, Summer, Golden Egg Hybrid": 1,
              "Cucumber, Supremo Hybrid": 4,
              "Cucumber, Sugar Crunch Hybrid": 4,
              "Cilantro, Calypso": 3,
              "Bunching Onion, Evergreen Long White Organic": 2,
              "Mesclun, Classic Mix": 1,
              "Arugula, Rocket (Roquette)": 1,
              "Radish, Perfecto": 1,
              "Tomato, Cherry Baby Hybrid": 2,
              #"thai basil": 1,
              "Lavender, Lady": 1,
              "Rosemary, Arp": 1,
              "Verbena, Lemon": 1,
              #"shiso": 1,
              "Chives": 2,
              "alpine stawberry": 2,
              "Pea, Easy Peasy": 1,
              "Pea, Sugar Snap": 2,
              "Corn, Ambrosia Hybrid": 3,
              "Cantaloupe, Burpee's Ambrosia Hybrid": 1,
              "Honeydew, Dolce Nectar Hybrid": 1,
              "Calendula, Pacific Beauty Mix Organic": 2,
              "Celery, Tall Utah 52-70R Improved": 1,
              "Pumpkin, Small Sugar": 1,
              "Oregano, Greek": 2,
              "Tarragon, Mexican": 1,
              "Sage, Common": 1,
              "Thyme, Common": 2,
              "Dill, Mammoth": 2,
              "Pepper, Hot, Habanero": 1,
              "Pepper, Hot, Serrano Chili": 1,
              "Pepper, Hot, Big Guy Hybrid": 1,
              "Pepper, Hot, Pepperoncini Greek": 1,
              #"zucchini": 2,
              "Eggplant, Millionaire Hybrid": 1,
              "Chinese Cabbage, Pak Choi, Toy Choi Hybrid": 2,
              "Fennel, Florence": 1,
              "Brussels Sprouts, Octia Hybrid": 1,
              "Garlic, Extra Select": 1,
              "Horseradish, Maliner Kren": 1,
              "Leek, Dawn Giant": 1,
              "Okra, Clemson Spineless": 1,
              "Parsnip, Hollow Crown": 1,
              "Turnip, Purple Top White Globe": 1,
              "Watermelon, Georgia Rattlesnake": 1}
"""

# not used for anything but kept as reference
families = ["brassicas", # cabbage family
            "legumes", # pea and bean family
            "chenopodiaceae", # beat family
            "cucurbits", # squash family
            "umbelliferae", # carrot and root family
            "solanaceae", # potato and tomato family
            "allium"] # onion family 

