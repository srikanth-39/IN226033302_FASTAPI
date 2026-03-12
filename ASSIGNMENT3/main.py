from fastapi import FastAPI,Query,Response,status
from pydantic import BaseModel,Field

app=FastAPI()

#-----Products database-----------------
products = [

    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},

    {'id': 2, 'name': 'Notebook',       'price':  99, 'category': 'Stationery',  'in_stock': True},

    {'id': 3, 'name': 'USB Hub',        'price': 799, 'category': 'Electronics', 'in_stock': False},

    {'id': 4, 'name': 'Pen Set',        'price':  49, 'category': 'Stationery',  'in_stock': True}
]


#-----------------Audit--------------------------------------
@app.get('/products/audit')
def product_audit(): 
    in_stock_list = [p for p in products if p['in_stock']]
    out_stock_list = [p for p in products if not p['in_stock']]
    stock_value = sum(p['price'] * 10 for p in in_stock_list)
    priciest = max(products, key=lambda p: p['price'])
    return { 'total_products': len(products), 'in_stock_count': len(in_stock_list),
    'out_of_stock_names': [p['name'] for p in out_stock_list], 'total_stock_value': stock_value, 'most_expensive': {'name': priciest['name'], 'price': priciest['price']}, }

#-------For checking the existing products-------------
@app.get("/products")
def get_products():
    return products


#---------Adding Products to the database----------------
class NewProduct(BaseModel):
    name : str =Field(...,min_length=3,max_length=17)
    price: int =Field(...,gt=0)
    in_stock :bool=True
    category :str=Field(...,min_length=5,max_length=17)


@app.post('/products/add')
def add_product(new_product: NewProduct,response: Response):
    existing_names = [p['name'] for p in products]

    if new_product.name in existing_names:
        response.status_code=status.HTTP_400_BAD_REQUEST
        return{'error': 'Product with this name already exists'}

    else:
        next_id=max(p['id'] for p in products)+1
        product={
            'id': next_id,
            'name': new_product.name,
            'price':new_product.price,
            'category': new_product.category,
            'in_stock':new_product.in_stock}

        products.append(product)
        response.status_code=status.HTTP_201_CREATED
        return{"message":"Product added","product":product}


#-------------Updating the product in_stock or price
@app.put('/products/update/{product_id}')
def update_product(
    product_id: int,
    response :Response,
    in_stock: bool=Query(None,description='Update stock status'),
    price: int=Query(None,description='Update price')):
    product=None
    for p in products:
        if p['id']==product_id:
            product=p
            break
    if not product:
        response.status_code=status.HTTP_404_NOT_FOUND
        return{'error': 'Product not found'}

    if in_stock is not None:
        product['in_stock']=in_stock

    if price is not None:
        product['price']=price

    return {"message":"producted updated","product":product}

#-------------------Deleting an item from the products-----------------
@app.delete('/products/delete/{product_id}')
def deleteItem(product :int ,response:Response):
    item=None
    for p in products:
        if p['id']==product:
            item=p 
            break
    if not item:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'error': 'Product not found'}

    else:
        products.remove(item)
        return {'message': f"Product '{item['name']}' deleted"}


#------------------CRUD OPERATIONS----------------------------------

#CRUD.1------adding the single product (already existing)------------------------
#CRUD.3------Checking for the all products------------------------
#CRUD.3------Checking for the single product------------------------
@app.get('/products/{product_id}')
def get_product(product_id :int,response :Response):
    product=None
    for p in products:
        if p['id']==product_id:
            product=p 
            break
    if not product:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"product with id": "{product_id} not found"}
    else:
        return{"product found": product}

#CRUD.4-----------Updating the product (already existing)------------------
#CRUD.5----------Verifying the product (already existing)------------------
#CRUD.6----------------Deleting the product (already existing)------------


#---------------BONUS--------------------------------------------------
@app.put('/products/discount')
def apply_discount(
    category: str = Query(..., description="Category to apply discount"),
    discount_percent: float = Query(..., gt=0, lt=100, description="Discount percentage")
):
    
    updated_products = []

    for p in products:
        if p['category'] == category:
            discount_amount = p['price'] * (discount_percent / 100)
            p['price'] = int(p['price'] - discount_amount)
            updated_products.append(p)

    return {
        "message": f"{discount_percent}% discount applied to {category} products",
        "updated_products": updated_products
    }




    












