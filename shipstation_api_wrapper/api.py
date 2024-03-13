import requests
from .filter import ShipStationOrderFilter, ShipStationProductFilter
from .models.order import CustomsItem
from typing import List
class ShipStationRequest:
    def __init__(self, base_url="https://ssapi.shipstation.com", headers=None):
        self.base_url = base_url
        self.headers = headers

    def get(self, endpoint, params=None)->requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return response
    def post(self, endpoint, json, params=None)->requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, json=json, params=params)
        return response
    def put(self, endpoint, json, params=None)->requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = requests.put(url, headers=self.headers, json=json, params=params)
        return response

class ShipStationClient:
    def __init__(self, api_key, base_url="https://ssapi.shipstation.com"):
        self.headers = headers={"Content-Type": "application/json", "Authorization": f"Basic {api_key}"}
        request_handler = ShipStationRequest(base_url, headers)
        self.tags = ShipStationTags(request_handler)
        self.orders = ShipStationOrders(request_handler)
        self.shipments = ShipStationShipments(request_handler)
        self.customers = ShipStationCustomers(request_handler)
        self.products = ShipStationProducts(request_handler)

class ShipStationTags:
    def __init__(self, request_handler: ShipStationRequest):
        self.request = request_handler

    def list(self):
        return self.request.get('/accounts/listtags') 
    
class ShipStationOrders:
    def __init__(self, request_handler: ShipStationRequest):
        self.request = request_handler
        
    def get_by_id(self, order_id): 
        return self.request.get(f'/orders/{order_id}')
    
    def list(self):
        return self.request.get('/orders')
    
    def list_with_filter(self, order_filter:ShipStationOrderFilter): 
        assert type(order_filter) == ShipStationOrderFilter, "filter type must be ShipStationOrderFilter"
        params = order_filter.get_filters()
        return self.request.get('/orders', params=params) 
    
    def get_by_number(self, order_number):
        order_filter = ShipStationOrderFilter()
        order_filter.add_order_number(order_number)
        return self.list_with_filter(order_filter=order_filter)

    def tag(self, order_id, tag_id): 
        return self.request.post('/orders/addtag', {'orderId': order_id, 'tagId': tag_id})

    def hold(self, order_id, date): 
        return self.request.post(f'/orders/holduntil', {'orderId': order_id, 'holdUntilDate': date})
    
    def add_note(self, note:str, order:dict):
        assert isinstance(order, dict), "order must be a shipstation order dictionary"
        assert 'internalNotes' in order, "order must contain internalNotes. Make sure you're passing an individual order, not list of orders." 

        new_note = {"internalNotes": f" {note} {order['internalNotes']}"}
        order.update(new_note)
        return self.request.post('/orders/createorder', order)

    def activate_saturday_delivery(self, order: dict, activate:bool):
        assert isinstance(order, dict), "order must be a shipstation order dictionary"
        assert 'advancedOptions' in order, "order must contain advancedOptions. Make sure you're passing an individual order, not list of orders." 
        
        sat_delivery = {"saturdayDelivery": activate}
        order['advancedOptions'].update(sat_delivery)
        return self.request.post('/orders/createorder', order)
    
    def update_customs_declaration(self, order: dict, custom_declarations:List[CustomsItem]):
        assert isinstance(order, dict), "order must be a shipstation order dictionary"
        assert 'advancedOptions' in order, "order must contain advancedOptions. Make sure you're passing an individual order, not list of orders."
        assert isinstance(custom_declarations, list), "custom_declaration must be a list of CustomsItem objects"
        assert type(custom_declarations[0]) == CustomsItem, "custom_declaration must be a CustomsItem object"
        
        order['internationalOptions']['customsItems'] = [c_d.model_dump() for c_d in custom_declarations]
        return self.request.post('/orders/createorder', order)

class ShipStationShipments:
    def __init__(self, request_handler: ShipStationRequest):
        self.request = request_handler
        
    def list(self):
        return self.request.get('/orders')
    
class ShipStationCustomers:
    def __init__(self, request_handler: ShipStationRequest):
        self.request = request_handler
        
    def list(self, stateCode=None, countryCode=None, marketplaceId=None, tagId=None, sortBy=None, sortDir=None, page=None, pageSize=None):
        # Construct the query parameters based on provided arguments
        params = {}
        if stateCode is not None:
            params['stateCode'] = stateCode
        if countryCode is not None:
            params['countryCode'] = countryCode
        if marketplaceId is not None:
            params['marketplaceId'] = marketplaceId
        if tagId is not None:
            params['tagId'] = tagId
        if sortBy is not None:
            params['sortBy'] = sortBy
        if sortDir is not None:
            params['sortDir'] = sortDir
        if page is not None:
            params['page'] = page
        if pageSize is not None:
            params['pageSize'] = pageSize
        return self.request.get('/customers', params=params)

    def get_by_id(self, customer_id): 
        return self.request.get(f'/customers/{customer_id}')

class ShipStationProducts: 
    def __init__(self, request_handler: ShipStationRequest):
        self.request = request_handler
    
    def list_products(self): 
        return self.request.get('/products')

    def get_product_by_sku(self, sku):
        filter = ShipStationProductFilter()
        filter.add_sku_filter(sku)
        params = filter.get_filters()
        return self.request.get(f'/products', params=params)
    
    def update_tag(self, sku:str, tag_ids:list):
        assert isinstance(tag_ids, list), "tag_ids must be a list"
        
        response_data = self.get_product_by_sku(sku).json()
        product = response_data['products'][0]
        product.update({'tags': []})
        return self.request.put(f'/products/{product["productId"]}', json=product)