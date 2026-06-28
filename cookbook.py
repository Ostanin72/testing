cook_book = [
      ['Салат',
          [
            ['картофель', 100, 'гр.'],
            ['морковь', 50, 'гр.'],
            ['огурцы', 50, 'гр.'],
            ['горошек', 30, 'гр.'],
            ['майонез', 70, 'мл.'],
          ]
      ],
      ['Пицца',
          [
            ['сыр', 50, 'гр.'],
            ['томаты', 50, 'гр.'],
            ['тесто', 100, 'гр.'],
            ['бекон', 30, 'гр.'],
            ['колбаса', 30, 'гр.'],
            ['грибы', 20, 'гр.'],
          ],
      ],
      ['Фруктовый десерт',
          [
            ['хурма', 60, 'гр.'],
            ['киви', 60, 'гр.'],
            ['творог', 60, 'гр.'],
            ['сахар', 10, 'гр.'],
            ['мед', 50, 'мл.'],
          ]
      ]
    ]


def solve(cook_book: list, person: int):
    result = []
    for dish in cook_book:
        dish_recipe = f"{dish[0]}: " # добавить в результат заголовок блюда
        for index, ingredient in enumerate(dish[1]):
            # собрать рецепт через пробел. число перевести в строку
            dish_recipe += " ".join([ingredient[0], str(ingredient[1] * person), ingredient[2]])
            if index < len(dish[1]) -1: # добавить запятую после ингредиента
                dish_recipe += ", "
        result.append(dish_recipe)
    return result

if __name__ == '__main__':
    result = solve(cook_book, 5)
    print(f"Список покупок на 5 персон: {result}")
