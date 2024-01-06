import pulp

# Constants
NAME = "Name"
RATIO = "Ratio"
WEIGHT = "Weight"
EXCLUDED_KEYS = [NAME, RATIO, WEIGHT]
ARMOR_ORDER = ["Helmet", "Chest", "Gauntlet", "Pants"]


class ArmorOptimizer:
    """
    A class used to optimize armor configuration based on given constraints and values to maximize.
    """

    def __init__(self, armor_data, weight_cap):
        """
        Initialize the ArmorOptimizer with armor data and weight cap.
        """
        self.armor_data = armor_data
        self.weight_cap = weight_cap

    def optimize_armor_configuration(self, value_to_maximize):
        """
        Optimize the armor configuration based on the value to maximize.
        """
        prob = pulp.LpProblem("Armor_Optimization", pulp.LpMaximize)
        armor_vars = pulp.LpVariable.dicts(
            "Armor",
            (
                (slot, armor[NAME])
                for slot in self.armor_data
                for armor in self.armor_data[slot]
            ),
            cat="Binary",
        )
        prob += pulp.lpSum(
            armor[value_to_maximize] * armor_vars[(slot, armor[NAME])]
            for slot in self.armor_data
            for armor in self.armor_data[slot]
        )
        prob += (
            pulp.lpSum(
                armor[WEIGHT] * armor_vars[(slot, armor[NAME])]
                for slot in self.armor_data
                for armor in self.armor_data[slot]
            )
            <= self.weight_cap
        )
        for slot in self.armor_data:
            prob += (
                pulp.lpSum(
                    armor_vars[(slot, armor[NAME])] for armor in self.armor_data[slot]
                )
                == 1
            )
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        optimal_configuration = {
            (slot, armor_name)
            for (slot, armor_name), armor_var in armor_vars.items()
            if pulp.value(armor_var) == 1
        }
        return optimal_configuration

    def calculate_total_stats(self, optimal_configuration):
        """
        Calculate the total stats for the optimal configuration.
        """
        total_stats = {
            key: sum(
                armor.get(key, 0)
                for slot, armor_name in optimal_configuration
                for armor in self.armor_data[slot]
                if armor[NAME] == armor_name
            )
            for key in self.armor_data[next(iter(self.armor_data.keys()))][0].keys()
            if key not in EXCLUDED_KEYS
        }
        return total_stats

    def print_optimal_configuration(self, optimal_configuration, total_stats):
        """
        Print the optimal configuration and total stats.
        """
        print("\nOptimal Armor Configuration:")
        for slot in ARMOR_ORDER:
            armor_name = next(
                (
                    name
                    for slot_name, name in optimal_configuration
                    if slot_name == slot
                ),
                None,
            )
            if armor_name:
                print(f"{slot}: {armor_name.title()}")
        print("\nTotal Stats:")
        stats_items = list(total_stats.items())
        for i in range(0, len(stats_items), 4):
            row_items = stats_items[i : i + 4]
            for stat, value in row_items:
                print(f"{stat}: {round(value, 2)}", end="\t")
            print()
