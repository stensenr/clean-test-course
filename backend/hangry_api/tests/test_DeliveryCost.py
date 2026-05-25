from api.controllers import Delivery
from django_mock_queries.query import MockSet, MockModel
import pytest


def build_order(*quantities):
  order = MockSet()
  for quantity in quantities:
    order.add(MockModel(quantity=quantity))
  return order

def test_LotsOfItems():
  #Arrange
  order = build_order(5, 5, 5)
  delivery_distance = 6
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 7.5

def test_MiddleOfTheRoadItems():
  #Arrange
  order = build_order(2, 2, 2)
  delivery_distance = 4
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 5

def test_LittleItems():
  #Arrange
  order = build_order(1, 2)
  delivery_distance = 2
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 3.5

def test_EmptyOrderGetsMinimumDeliveryCost():
  #Arrange
  order = build_order()
  delivery_distance = 10
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 3.5

def test_ExactlyFiveItemsAndThreeMilesGetsMinimumDeliveryCost():
  #Arrange
  order = build_order(2, 3)
  delivery_distance = 3
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 3.5

def test_ExactlyTenItemsAndFiveMilesGetsMiddleDeliveryCost():
  #Arrange
  order = build_order(5, 5)
  delivery_distance = 5
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 5

def test_MoreThanTenItemsButFiveMilesGetsMiddleDeliveryCost():
  #Arrange
  order = build_order(6, 5)
  delivery_distance = 5
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 5

def test_MoreThanFiveMilesButOnlyTenItemsGetsMiddleDeliveryCost():
  #Arrange
  order = build_order(5, 5)
  delivery_distance = 6
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 5

def test_MoreThanFiveItemsButOnlyThreeMilesGetsMinimumDeliveryCost():
  #Arrange
  order = build_order(3, 3)
  delivery_distance = 3
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 3.5

def test_NegativeDistanceGetsMinimumDeliveryCost():
  #Arrange
  order = build_order(20)
  delivery_distance = -1
  #Act
  cost = Delivery.calculate(order,delivery_distance)
  #Assert
  assert cost == 3.5

def test_ItemWithoutQuantityRaisesTypeError():
  #Arrange
  order = MockSet()
  order.add(MockModel())
  #Act / Assert
  with pytest.raises(TypeError):
    Delivery.calculate(order,1)

def test_NoneOrderRaisesTypeError():
  #Act / Assert
  with pytest.raises(TypeError):
    Delivery.calculate(None,1)

def test_NonNumericDistanceRaisesTypeErrorWhenDistanceCompared():
  #Arrange
  order = build_order(6)
  #Act / Assert
  with pytest.raises(TypeError):
    Delivery.calculate(order,"far")
