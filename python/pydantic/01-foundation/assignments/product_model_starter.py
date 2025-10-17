from pydantic import BaseModel

# TODO: Create Product model with id, name, price, in_stock

class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

input_data = {'id': 1, 'name': "Laptop", 'price': 999.99, 'in_stock': True}
product = Product(**input_data)