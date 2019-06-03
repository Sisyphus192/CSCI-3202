GARDEN PLANNING TOOL README

REQUIREMENTS:
-Numpy
-BeautifulSoup4 (only for webscrapper to fetch data once, not needed to run CSP solver)

FILES:

config.py
- Contains dictionaries of the pre-planned gardens beds from www.gardeners.com

csp.py 
- Contains the CSP problem class object and backtracking and related functions. Both the CSP class and backtracking_search functions were written to be generic enough to be used for any CSP but this was not tested.

garden.py
- The Plant class which handles all the plant data and parsing from the json file.
- The Garden class which inherits from CSP, tracks which plants are to be planted in the garden
	as well as verious garden properties. Also implements the garden constraint method which checks
	arc-consistency between two variables.

util.py
-web scraper function for Burpee.com to grab the plant data and save to json file (used once) and a function to lookup the common name of a plant (e.g. "")

companions.json
-contains companion plant data scarped from Wikipedia

plants.json
-contains plant data scraped from Burpee.com

1. USAGE

The tool has a console based menu and does not take command line arguments.
Run "python3 garden.py" to start the planning tool.

You will be presented with the following options:

1. Optimize a preplanned garden

Several of the preplanned square foot gardens from www.gardeners.com were implemented
however, those gardens are layed out in an aesthetically pleasing way, and are not
optimal by our standards of height and companion planting.

You will then be asked to select the direction from which the sun predominantly shines on the garden.

The planning tool will then try to optimize the layout of the garden based on the layout of the garden
bed, selected plants, and sun direction. Not all the preplanned gardens can be optimized in this way.

2. Run the test suite
This will take a bit to run, but it will run the solver over all the pre-planned gardens
several time and average the results. Used for testing perfomance improvements from 
various heuristics

You can add your own garden if you so choose to the the pre-planned gardens dictionary in config.py