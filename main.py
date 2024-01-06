from armor_optimizer import ArmorOptimizer
from utils import load_armor_data, get_armor_attributes, get_user_selected_attribute


def main():
    """
    Main function to run the armor optimization.
    """
    weight_cap = float(input("Enter the weight cap: "))
    armor_data = load_armor_data()
    armor_attributes = get_armor_attributes(armor_data)
    selected_attribute = get_user_selected_attribute(armor_attributes)
    optimizer = ArmorOptimizer(armor_data, weight_cap)
    optimal_configuration = optimizer.optimize_armor_configuration(selected_attribute)
    total_stats = optimizer.calculate_total_stats(optimal_configuration)
    optimizer.print_optimal_configuration(optimal_configuration, total_stats)


if __name__ == "__main__":
    main()
