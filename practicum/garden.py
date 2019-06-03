"""
This file contains the following classes:
    Garden - a CSP subclass for garden properties and layout
    Plant - for plant objects to be planted
"""

import json
import re
import numpy as np
import csp
from config import preplanned_gardens
from util import get_common_name

# loads the compainion plant data scrapped from wikipedia
with open("companions.json") as in_file:
    companions = json.load(in_file)

class Plant:
    """
    This class is probably overengineered for the scope of the problem.
    Plant data was scrapped from burpee.com from a predefined list and
    saved in plants.json. The constructor of this class parses the json values
    into the appropriate values. This data was not parsed beforehand in case I
    needed the full information (e.g. the range of the plant height rather than just the max).
    """
    def __init__(self, name, plant):
        self.name = name
        self.sun = plant["Sun"]
        if "Life Cycle" not in plant:
            self.life_cycle = None
        else:
            self.life_cycle = plant["Life Cycle"]
        if "Days To Maturity" not in plant:
            self.days_to_maturity = None
        else:
            if "-" in plant["Days To Maturity"]:
                self.days_to_maturity = int(re.split(r'[-\s]', plant["Days To Maturity"])[1])
            else:
                self.days_to_maturity = int(re.split(r'[-\s]', plant["Days To Maturity"])[0])
        if "-" in plant["Height"]:
            self.height = int(re.split(r'[-\s]', plant["Height"])[1])
        else:
            self.height = int(re.split(r'[-\s]', plant["Height"])[0])
        if "-" in plant["Spread"]:
            self.spread = int(re.split(r'[-\s]', plant["Spread"])[1])
        else:
            self.spread = int(re.split(r'[-\s]', plant["Spread"])[0])
        self.sow_method = plant["Sow Method"]
        if "Sow Time" not in plant:
            self.sow_time = None
        else:
            self.sow_time = plant["Sow Time"]
        self.family = None
        if "Germination" not in plant:
            self.germination = None
        else:
            self.germination = plant["Germination"]
        if "Transplant" not in plant:
            self.transplant = None
        else:
            self.transplant = plant["Transplant"]
        if "Thin" not in plant:
            self.thin = None
        else:
            self.thin = int(re.split(r'\s', plant["Thin"])[0])
        self.common_name = get_common_name(self.name)

    def __eq__(self, other):
        """
        Plants are equivalent if they have the same name
        """
        if isinstance(other, Plant):
            return self.name == other.name
        return False

    def __repr__(self):
        return self.name

    def __str__(self):
        str_ = ""
        str_ += self.name + "\n"
        str_ += "Sun: " + self.sun + "\n"
        str_ += "Life Cycle: " + str(self.life_cycle) + "\n"
        str_ += "Spread: " + str(self.spread) + "\n"
        str_ += "Days to Maturity: " + str(self.days_to_maturity) + "\n"
        str_ += "Height: " + str(self.height) + "\n"
        str_ += "Spread: " + str(self.spread) + "\n"
        str_ += "Sow Method: " + str(self.sow_method) + "\n"
        str_ += "Family: " + str(self.family) + "\n"
        str_ += "Germination: " + str(self.germination) + "\n"
        str_ += "Transplant: " + str(self.transplant) + "\n"
        str_ += "Thin: " + str(self.thin)
        return str_

class Garden(csp.CSP):
    """
    Make a CSP for creating a garden plan.
    """
    def __init__(self, garden_selection=None, direction_selection=None):
        # load scapped plant data
        with open('plants.json') as in_file:
            self.plant_data = json.load(in_file)

        # set layout and plant selection
        if garden_selection is not None:
            self.layout = np.full(garden_selection["size"], 0)
            self.selected_plants = garden_selection["plants"]
        else:
            self.layout = np.full([3, 14], 0)
            self.layout[:, 6:8] = -1
        # set direction sun shines across garden
        if direction_selection is not None:
            self.sun_positions = direction_selection
        else:
            self.sun_positions = "South-East"

        # setup parameters for CSP
        self.vars_x = []
        self.domains = {}
        self.neighbors = {} # to explicitly define adjacent squares in the garden
        for (x, y), value in np.ndenumerate(self.layout):
            if self.layout[x, y] != -1: # -1 is reserved for non-plantable space and is not a valid var
                self.vars_x.append((x, y))
                # the domain for each var is a list of plants that can go in that square
                self.domains[(x, y)] = [Plant(plant, self.plant_data[plant]) for plant in self.selected_plants]
                # enumerate the neighbors of each square in the bed
                self.neighbors[(x, y)] = []
                if x - 1 >= 0:
                    if self.layout[x - 1, y] != -1:
                        self.neighbors[(x, y)].append((x - 1, y))
                if y - 1 >= 0:
                    if self.layout[x, y - 1] != -1:
                        self.neighbors[(x, y)].append((x, y - 1))
                if x + 1 < self.layout.shape[0]:
                    if self.layout[x + 1, y] != -1:
                        self.neighbors[(x, y)].append((x + 1, y))
                if y + 1 < self.layout.shape[1]:
                    if self.layout[x, y + 1] != -1:
                        self.neighbors[(x, y)].append((x, y + 1))
        # finally initialize base CSP class
        #print("Creating a CSP with the following garden: ")
        #print("Layout:\n", self.layout)
        #print("Selected plants:\n", self.selected_plants)
        #print("Positions of the sun:\n", self.sun_positions)
        csp.CSP.__init__(self, self.vars_x, self.domains, self.neighbors, self.garden_constraint)

    def garden_constraint(self, var_a, val_a, var_b, val_b, assignment):
        """
        Used by the CSP to evaluate constraints, the constraints are:
            - Plants must be arranged shortest to tallest in two axis
            (e.g. north-south, east-west), for the directions the sun
            faces the garden. This ensures shorter plants are not shaded
            by taller plants.
            - Plants must not be adjacent to plants they are not compatible with,
            unlike with sunlight direction this adjecency will include diagonals.
        """

        # the following checks the global constraints of maximum number of plants for certain types
        assigned_plants = {}
        for variable in assignment:
            if assignment[variable].name not in assigned_plants:
                assigned_plants[assignment[variable].name] = 1
            else:
                assigned_plants[assignment[variable].name] += 1
        if val_a.name not in assigned_plants:
            assigned_plants[val_a.name] = 1
        else:
            assigned_plants[val_a.name] += 1
        for plant, num in assigned_plants.items():
            if num > self.selected_plants[plant]:
                return False

        # the following checks the binary constraint of not having certain plants adjacent to each other
        """
        val_a_found = False
        val_b_found = False
        if val_a.common_name is not None and val_b.common_name is not None:
            for i in companions:
                if i["Common name"] == val_a.common_name:
                    val_a_found = True
                    if val_b.common_name.lower() in i["Avoid"]:
                        #print("{} should not be planted next to {}".format(val_a.name, val_b.name))
                        return False
                if  i["Common name"] == val_b.common_name:
                    val_b_found = True
                    if val_a.common_name.lower() in i["Avoid"]:
                        #print("{} should not be planted next to {}".format(val_a.name, val_b.name))
                        return False
                if val_a_found and val_b_found:
                    break
        """
        # the following checks the binary height contraints
        if "North" in self.sun_positions: # we assume equal light from east and west
            if var_a[0] < var_b[0]: # square A is north of square B
                if val_a.height >= val_b.height:
                    return False
            elif var_a[0] > var_b[0]: #square B is north of square A
                if val_a.height <= val_b.height:
                    return False
        if "East" in self.sun_positions: # we don't assume equal light from north and south, because axial tilt
            if var_a[1] > var_b[1]: # square A is east of square B
                if val_a.height > val_b.height:
                    return False
            elif var_a[1] < var_b[1]: #square B is east of square A
                if val_a.height < val_b.height:
                    return False
        if "South" in self.sun_positions: # we assume equal light from east and west
            if var_a[0] > var_b[0]: # square A is south of square B
                if val_a.height >= val_b.height:
                    return False
            elif var_a[0] < var_b[0]: #square B is south of square A
                if val_a.height <= val_b.height:
                    return False
        if "West" in self.sun_positions: # we don't assume equal light from north and south, because axial tilt
            if var_a[1] < var_b[1]: # square A is west of square B
                if val_a.height > val_b.height:
                    return False
            elif var_a[1] > var_b[1]: #square B is west of square A
                if val_a.height < val_b.height:
                    return False
        return True

    def __str__(self):
        np.set_printoptions(linewidth=np.inf)
        return str(self.layout)


def test_suite():
    """
    This function will run through all the pre-planned garden beds from
    gardeners.com several times and average the results for each.
    It was used to test performance improvement
    """
    print("Running test suite, this will take some time... (15-25 minutes depending on computer speed)")
    print("Selecting default sun facing of South")
    print("Enabling minimum-remaining-values heuristic")
    print("Enabling degree heuristic")
    print("Enabling least contraining value heuristic")
    direction_selection = "South"
    results = {}
    for g in preplanned_gardens:
        counts = []
        success_rate = []
        for i in range(10):
            garden = Garden(preplanned_gardens[g], direction_selection)
            garden.minimum_remaining_values = True
            garden.degree_heuristic = True
            garden.least_constraining_value = True
            plan, cnt = csp.backtracking_search(garden)
            if plan is None:
                success_rate.append(False)
            else:
                success_rate.append(True)
            counts.append(cnt)
        results[g] = {"success_rate": "{}".format(success_rate.count(True)/len(success_rate)), "time": int(sum(counts)/len(counts))}
    print("\n")
    for g in results:
        print(g)
        print(results[g])
    print("Success rate is the fraction of times a solution was found within the time contraints")
    print("A solution may not exists for all scenerios")
    print("'time' is the number of calls to backtrack()")


def optimize_preplanned():
    print("Which garden?")
    for idx, garden in enumerate(preplanned_gardens):
        print("{}. {}".format(idx, garden))
    while True:
        try:
            choice = int(input(">> "))
            garden_selection = preplanned_gardens[list(preplanned_gardens.keys())[int(choice)]]
        except ValueError:
            print("Invalid Input")
            continue
        except IndexError:
            print("Invalid Selection")
            continue
        else:
            break
    directions = ["North", "East", "South", "West", "North-East", "North-West", "South-East", "South-West"]
    print("From what direction does the sun predominatly shine on the garden?")
    for idx, direction in enumerate(directions):
        print("{}. {}".format(idx, direction))
    while True:
        try:
            choice = int(input(">> "))
            direction_selection = directions[choice]
        except ValueError:
            print("Invalid Input")
            continue
        except IndexError:
            print("Invalid Selection")
            continue
        else:
            break

    garden = Garden(garden_selection, direction_selection)
    print("Creating a CSP with the following garden: ")
    print("Layout:\n", garden.layout)
    print("Selected plants:\n", garden.selected_plants)
    print("Positions of the sun:\n", garden.sun_positions)

    garden.minimum_remaining_values = False
    garden.degree_heuristic = False
    garden.least_constraining_value = False
    plan, cnt = csp.backtracking_search(garden)
    if plan is None:
        print("Unable to create garden plan that satisfies all constraints")
    else:
        print("plan: ", plan)
        for a in plan:
            garden.layout[a[0], a[1]] = int(plan[a].height)
        print(garden.layout)

def main():
    print("Welcome to the Square Foot Gardening Optimizer by Dereks\n")
    print("1. Optimize pre-planned garden from www.gardeners.com")
    print("2. Run test suite on pre-planned gardens")
    print("3. Quit")
    while True:
        try:
            choice = int(input(">> "))
        except ValueError:
            print("Invalid Input")
            continue
        else:
            break
    if choice == 1:
        optimize_preplanned()
    if choice == 2:
        test_suite()


if __name__ == "__main__":
    main()
