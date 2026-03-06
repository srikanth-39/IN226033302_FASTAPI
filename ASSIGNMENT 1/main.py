from fastapi import FastAPI,Query

 

app = FastAPI()

 

# ── Endpoint 1-Adding the 3 items our database for now ──────────

products = [

    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },

    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },

    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},

    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
   {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True}, 
   {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}

]

 

# ── Endpoint 0 — Home ────────────────────────────────────────

@app.get('/')

def home():

    return {'message': 'Welcome to our E-commerce API'}

 

# ── Endpoint 2 — Return the filtered product ──────────────────────────

@app.get('/products')

def get_all_products():

    return {'products': products, 'total': len(products)}


@app.get('/products/filter')

def filter_products(

    category:  str  = Query(None, description='Electronics or Stationery'),

    max_price: int  = Query(None, description='Maximum price'),

    in_stock:  bool = Query(None, description='True = in stock only')

):

    result = products          # start with all products

 

    if category:

        result = [p for p in result if p['category'] == category]

 

    if max_price:

        result = [p for p in result if p['price'] <= max_price]

 

    if in_stock is not None:

        result = [p for p in result if p['in_stock'] == in_stock]

    if len(result)==0:
        return {"error": "No products found in this category"}

    return {'filtered_products': result, 'count': len(result)}






# ── Endpoint 3 — Return one product if it in the stock──────────────────

@app.get('/products/instock')

def get_instock():

    available=[p for p in products if p["in_stock"]==True ]
    return {"in_stock_products": available, "count": len(available)}

#--------Endpoint 4 - Return the summary of the store----------
@app.get('/store/summary')

def get_summary():
    tp=len(products)
    ins=len([p for p in products if p["in_stock"]==True])
    ofs=tp-ins
    cat=list(set([p["category"] for p in products]))




    return { "store_name": "My E-commerce Store", "total_products": tp, "in_stock": ins, "out_of_stock": ofs,"categories": cat }


#----------Endpoint 5-Search product by the name-----------
@app.get('/products/search/{keyword}')
def get_search(keyword : str):
    res=[p for p in products if keyword.lower() in p["name"].lower()]
    
    if not res:
        return {"message": "No products matched your search"} 
    return{"keyword": keyword, "results": res, "total_matches": len(res)}


#---------Endpoint Bonus Cheapest & Most Expensive Product---------
@app.get('/products/deals')
def get_deals():
    c=products[0]
    m=products[0]
    for i in range(len(products)):
        if products[i]['price']<c['price']:
            c=products[i]
        if products[i]['price']>m['price']:
            m=products[i]

    return{"Best Deal":c,'Premium Pick':m}




