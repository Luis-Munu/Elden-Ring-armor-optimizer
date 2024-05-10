from typing import Dict, List, Tuple, Union
import pulp

# Constants
NAME = "Name"
RATIO = "Ratio"
WEIGHT = "Weight"
EXCLUDED_KEYS = [NAME, RATIO, WEIGHT]
ARMOR_ORDER = ["Helmet", "Chest", "Gauntlet", "Pant"]
STATS_PER_ROW = 4


class ArmorOptimizer:
    """
    A class used to optimize armor configuration based on given constraints and values to maximize.

    Attributes
    ----------
    armor_data : Dict
        The data of the armor.
    weight_cap : float
        The weight cap of the armor.
    """

    def __init__(self, armor_data: Dict, weight_cap: float):
        """
        Constructs all the necessary attributes for the ArmorOptimizer object.

        Parameters
        ----------
            armor_data : Dict
                The data of the armor.
            weight_cap : float
                The weight cap of the armor.
        """
        if not armor_data:
            raise ValueError("Armor data cannot be empty.")
        if weight_cap < 0:
            raise ValueError("Weight cap cannot be negative.")
        self.armor_data = armor_data
        self.weight_cap = weight_cap

    def optimize_armor_configuration(self, value_to_maximize: str) -> Dict:
        """
        Optimize the armor configuration based on the value to maximize.

        Parameters
        ----------
            value_to_maximize : str
                The value to maximize.

        Returns
        -------
        Dict
            The optimal configuration of the armor.
        """
        # Create a linear programming problem for armor optimization
        prob = pulp.LpProblem("Armor_Optimization", pulp.LpMaximize)

        # Create binary variables for each armor piece in each slot
        armor_vars = pulp.LpVariable.dicts(
            "Armor",
            (
                (slot, armor[NAME])
                for slot in self.armor_data
                for armor in self.armor_data[slot]
            ),
            cat="Binary",
        )

        # The objective function is to maximize the sum of the value_to_maximize for each armor piece
        prob += pulp.lpSum(
            armor[value_to_maximize] * armor_vars[(slot, armor[NAME])]
            for slot in self.armor_data
            for armor in self.armor_data[slot]
        )

        # Add a constraint that the total weight of the armor pieces must be less than or equal to the weight cap
        prob += (
            pulp.lpSum(
                armor[WEIGHT] * armor_vars[(slot, armor[NAME])]
                for slot in self.armor_data
                for armor in self.armor_data[slot]
            )
            <= self.weight_cap
        )

        # Add a constraint that exactly one armor piece must be chosen for each slot
        for slot in self.armor_data:
            prob += (
                pulp.lpSum(
                    armor_vars[(slot, armor[NAME])] for armor in self.armor_data[slot]
                )
                == 1
            )

        # Solve the problem using the CBC solver
        prob.solve(pulp.PULP_CBC_CMD(msg=0))

        # Extract the optimal configuration from the solution
        optimal_configuration = {
            (slot, armor_name)
            for (slot, armor_name), armor_var in armor_vars.items()
            if pulp.value(armor_var) == 1
        }

        return optimal_configuration

    def calculate_total_stats(self, optimal_configuration: Dict) -> Dict:
        """
        Calculate the total stats for the optimal configuration.

        Parameters
        ----------
            optimal_configuration : Dict
                The optimal configuration of the armor.

        Returns
        -------
        Dict
            The total stats of the armor.
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

    def generate_optimal_configuration_output(
        self, optimal_configuration: Dict[str, str], total_stats: Dict[str, float]
    ) -> str:
        """
        Generate the output string for the optimal configuration and total stats.

        Parameters
        ----------
            optimal_configuration : Dict[str, str]
                The optimal configuration of the armor.
            total_stats : Dict[str, float]
                The total stats of the armor.

        Returns
        -------
        str
            The output string for the optimal configuration and total stats.
        """
        output = "\nOptimal Armor Configuration:\n"
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
                output += f"{slot}: {armor_name.title()}\n"
        output += "\nTotal Stats:\n"
        stats_items = list(total_stats.items())
        for i in range(0, len(stats_items), STATS_PER_ROW):
            row_items = stats_items[i : i + STATS_PER_ROW]
            for stat, value in row_items:
                output += f"{stat}: {round(value, 2)}\t"
            output += "\n"
        return output
