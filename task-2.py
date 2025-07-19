import pandas as pd
import random
import timeit
from BTrees.OOBTree import OOBTree

# Завантаження CSV (заміни шлях, якщо потрібно)
try:
    df = pd.read_csv("generated_items_data.csv")
except FileNotFoundError:
    # Створення фейкових даних, якщо файл відсутній
    print("CSV файл не знайдено. Створюємо випадкові дані.")
    num_items = 10000
    df = pd.DataFrame({
        "ID": [i for i in range(num_items)],
        "Name": [f"Item {i}" for i in range(num_items)],
        "Category": [f"Category {i % 10}" for i in range(num_items)],
        "Price": [round(random.uniform(10, 1000), 2) for _ in range(num_items)],
    })

# Ініціалізація структур
tree = OOBTree()
dictionary = {}

# Додавання товарів
def add_item_to_tree(item_id, item_data):
    tree[item_id] = item_data

def add_item_to_dict(item_id, item_data):
    dictionary[item_id] = item_data

# Діапазонні запити
def range_query_tree(min_price, max_price):
    return [v for v in tree.values() if min_price <= v["Price"] <= max_price]

def range_query_dict(min_price, max_price):
    return [v for v in dictionary.values() if min_price <= v["Price"] <= max_price]

# Заповнення обох структур
for _, row in df.iterrows():
    item = {"Name": row["Name"], "Category": row["Category"], "Price": row["Price"]}
    add_item_to_tree(row["ID"], item)
    add_item_to_dict(row["ID"], item)

# Генерація випадкових цінових діапазонів
price_ranges = [(random.uniform(100, 300), random.uniform(301, 700)) for _ in range(100)]

# Вимірювання часу для OOBTree
tree_time = timeit.timeit(
    stmt="for r in price_ranges: range_query_tree(r[0], r[1])",
    globals=globals(),
    number=1
)

# Вимірювання часу для dict
dict_time = timeit.timeit(
    stmt="for r in price_ranges: range_query_dict(r[0], r[1])",
    globals=globals(),
    number=1
)

# Виведення результатів
print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
