import pytest
from praktikum.burger import Burger
from unittest.mock import Mock

class TestBurger:
    def test_set_buns_successful(self):
        burger = Burger()
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient_successful(self):
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1

    def test_remove_ingredient_successful(self):
        burger = Burger()
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 0

    @pytest.mark.parametrize('index,new_index', [[0, 2], [0, 0], [0, 1]])
    def test_move_ingredient_successful(self, index, new_index):
        burger = Burger()
        mock_ingredient_1 = Mock()
        mock_ingredient_2 = Mock()
        mock_ingredient_3 = Mock()
        burger.add_ingredient(mock_ingredient_1) #исходный индекс 0
        burger.add_ingredient(mock_ingredient_2) #исходный индекс 1
        burger.add_ingredient(mock_ingredient_3) #исходный индекс 2
        burger.move_ingredient(index, new_index)
        assert burger.ingredients[new_index] == mock_ingredient_1

    @pytest.mark.parametrize(
        'bun_price, ingredient_prices, expected_total', [
            [50.5, [], 101.0], [0.0, [], 0.0], [50.0, [15.0, 25.0, 100.0], 240], [50.0, [0.0], 100.0]
        ]
    )
    def test_get_price_successful(self, bun_price, ingredient_prices, expected_total):
        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        for price in ingredient_prices:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            burger.add_ingredient(mock_ingredient)

        assert burger.get_price() == expected_total

    @pytest.mark.parametrize(
        "ingredients_data, expected_result",[
            #Сценарий 1: Бургер без начинки
            [[], ["(==== Булочка ====)", "Price: 100.0"]],
            # Сценарий 2: Бургер с соусом и начинкой
            [[['СОУС', 'Терияки', 20.0], ['Начинка', 'сыр', 35.0]], ["(==== Булочка ====)", "= соус Терияки =", "= начинка сыр =", "Price: 155.0"]]
        ]
    )
    def test_get_receipt_successful(self, ingredients_data, expected_result):
        burger = Burger()

        mock_bun = Mock()
        mock_bun.get_name.return_value = 'Булочка'
        mock_bun.get_price.return_value = 50.0
        burger.set_buns(mock_bun)

        for type_ing, name_ing, price_ing in ingredients_data:
            mock_ingredient = Mock()
            mock_ingredient.get_type.return_value = type_ing
            mock_ingredient.get_name.return_value = name_ing
            mock_ingredient.get_price.return_value = price_ing
            burger.add_ingredient(mock_ingredient)

        receipt = burger.get_receipt()
        for part in expected_result:
            assert part in receipt
            
         
