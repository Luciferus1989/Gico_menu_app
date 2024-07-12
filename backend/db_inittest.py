import pandas as pd

data = {
    "ItemMenu": [
        "CHICKEN PARMIGIANA", "CHICKEN MILANESE", "DEEP FRIED CALAMARI", "WAGYU BEEF SANDO",
        "TEMPURA SOFTSHELL CRAB BURGER", "DEEP FRIED CHICKEN KATSU BURGER", "PANKO CHICKEN BURGER",
        "AMERICAN BURGER", "WAGYU BEEF RAGU BURGER", "VEGAN BURGER", "GRILLED SALMON",
        "GRILLED BARRAMUNDI", "BLACK MUSSELS", "GICO’S SPECIAL SEAFOOD PLATTER ORIGINAL SIZE",
        "GICO’S SPECIAL SEAFOOD PLATTER MEDIUM SIZE", "WAGYU BEEF SCALOPPINE FUNGHI",
        "WAGYU BEEF SALTIMBOCCA ALLA ROMANA", "PREMIUM SCOTCH FILLET", "MAYURA STATION MB5 PORTERHOUSE (250g)",
        "MAYURA STATION MBS7 SCOTCH FILLET  250G", "Kids spaghetti wagyu bolognaise", "Kids spaghetti napaletana",
        "Kids chips", "Kids fish and chips", "Kids chips and chicken nuggets", "Roasted cocktail potato with mixed herbs and salt",
        "Pan fried broccolini with fried shallots", "Deep fried corn ribs with seasoning", "Crunchy chips",
        "Sweet potato chips", "Wedges with sweet chill sauce and sour cream", "GARDEN SALAD",
        "GICO’S ISLAND GRILLED CHICKEN SALAD", "CHICKEN CAESAR SALAD", "Table tiramisu",
        "Mango and cardamom crème brulees", "Pandan bubble waffle"
    ],
    "description": [
        "Panko chicken, ham, cheese, mushroom sauce with Italian herb chips, salad.",
        "Chicken seasoned bread crumb mix with Italian herb chips, salad.",
        "Deep fried panko squid rings served with Italian herb chips, salad, tartare sauce.",
        "Wagyu beef slow cooked onions, tomato salsa with Italian herb chips and salad.",
        "Softshell crab, pineapple, red cabbage, tomato, pickles, cheese, burger sauce served with your choice of sweet potato chips or Italian herb chips.",
        "Crunchy chicken katsu, grilled pineapple, red cabbage, tomato, pickles, burger cheese, secret burger sauce served with your choice of sweet potato chips or Italian herb chips.",
        "Chicken breadcrumbs, pineapple, red cabbage, tomato, pickles, cheese, burger sauce served with your choice of sweet potato chips or Italian herb chips.",
        "Double beef patty, pineapple, red cabbage, tomato, pickles, cheese, burger sauce served with your choice of sweet potato chips or Italian herb chips.",
        "Oven slow cooked wagyu ragu, red cabbage, onion, carrot, burger sauce served with your choice of sweet potato chips or Italian herb chips.",
        "Kale, spinach, pumpkin, mushroom, pickle, burger sauce served with sweet potato chips.",
        "Grilled salmon, mash potato, tomato salsa, grill broccolini, chimichurri.",
        "Lentil cooked with wagyu meat balls, grilled broccolini, pumpkin, gremolata.",
        "Fresh tomato cooked with garlic, chill, white wine with Napoli sauce.",
        "Blue swimmer crab, black mussels, green mussels, clams, prawns, salmon, leatherjacket, cooked with garlic, spring onions, fresh tomato, basil, mixed herbs and Napoli sauce.",
        "Blue swimmer crab, black mussels, green mussels, clams, prawns, salmon, leatherjacket, cooked with garlic, spring onions, fresh tomato, basil, mixed herbs and Napoli sauce.",
        "Pan fried wagyu veal, mushroom sauce, served with vegetables and salad.",
        "Pan fried wagyu veal, prosciutto, asparagus, cheese, served with vegetables and salad.",
        "Cooked to your liking with mash potato and vegetables",
        "Cooked to your liking with mash potato and vegetables.",
        "Cooked to your liking with mash potato and vegetables. (Paired with Vinette shiraz)",
        "Wagyu beef mix, rich tomato base sauce, grilled steak, parmesan cheese (Paired with Turkey Flat GSM)",
        "Wagyu meat balls, tomato, herbs",
        "Truffle, mushroom, broad bean, ricotta, rose sauce",
        "Chicken, truffle, mushroom, broad bean, ricotta, rose sauce.",
        "Smoked leg ham, mushroom, truffle, cream sauce.",
        "Kids spaghetti napaletana",
        "Kids chips",
        "Kids fish and chips",
        "Kids chips and chicken nuggets",
        "Roasted cocktail potato with mixed herbs and salt",
        "Pan fried broccolini with fried shallots",
        "Deep fried corn ribs with seasoning",
        "Crunchy chips",
        "Sweet potato chips",
        "Wedges with sweet chill sauce and sour cream",
        "Cos lettuce, rocket, avocado, onion, tomato, cucumber, olive with light dressing on the side.",
        "Marinated chicken tenderloins, cos lettuce, avocado, tomato, cucumber, walnuts, with light dressing on the side.",
        "Cos lettuce, garlic croutons, bacon, poached egg, parmesan cheese, home-made dressing.",
        "Table tiramisu",
        "Mango and cardamom crème brulees",
        "Pandan bubble waffle"
    ],
    "category": [
        "Main", "Main", "Main", "Main", "Burger", "Burger", "Burger", "Burger", "Burger", "Burger",
        "Fish and Seafood", "Fish and Seafood", "Fish and Seafood", "Fish and Seafood", "Fish and Seafood",
        "Meat", "Meat", "Meat", "Meat", "Meat", "Kids Meal", "Kids Meal", "Kids Meal", "Kids Meal", "Kids Meal",
        "Side Dish", "Side Dish", "Side Dish", "Side Dish", "Side Dish", "Side Dish", "Salad", "Salad", "Salad",
        "Dessert", "Dessert", "Dessert"
    ],
    "price": [
        26, 26, 26, 26, 25, 24, 24, 26, 25, 24, 35, 35, 35, 90, 75, 35, 37, 39, 55, 59, 17, 14, 6, 16, 14, 16, 17,
        14, 9, 9, 12, 18, 24, 26, 16, 18, 21
    ]
}

# Проверяем длину списков
lengths = [len(data[key]) for key in data]
print("Lengths of lists:", lengths)

# Убедитесь, что все списки имеют одинаковую длину
min_length = min(lengths)
for key in data:
    data[key] = data[key][:min_length]

# Создаем DataFrame
df = pd.DataFrame(data)

# Сохранение в CSV файл
csv_file_path = "menu.csv"
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

