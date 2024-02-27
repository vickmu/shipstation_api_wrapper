import requests
from .filter import ShipStationOrderFilter
class ShipStationRequest:
    def __init__(self, base_url="https://ssapi.shipstation.com", headers=None):
        self.base_url = base_url
        self.headers = headers

    def get(self, endpoint, params=None)->requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        return response
    def post(self, endpoint, json)->requests.Response:
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=self.headers, json=json)
        return response

class ShipStationClient:
    def __init__(self, api_key, base_url="https://ssapi.shipstation.com"):
        self.headers = headers={"Content-Type": "application/json", "Authorization": f"Basic {api_key}"}
        request_handler = ShipStationRequest(base_url, headers)
        self.tags = ShipStationTags(request_handler)
        self.orders = ShipStationOrders(request_handler)
        self.shipments = ShipStationShipments(request_handler)
        self.customers = ShipStationCustomers(request_handler)

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
    
    def tag(self, order_id, tag_id): 
        return self.request.post('/orders/addtag', {'orderId': order_id, 'tagId': tag_id})

    def hold(self, order_id, date): 
        return self.request.post(f'/orders/holduntil', {'orderId': order_id, 'holdUntilDate': date})
    
    def add_note(self, note:str, order_id:int):
    
        order_data = self.get_by_id(order_id=order_id).json()['orders'][0]
        new_note = {"internalNotes": f" {note} {order_data['internalNotes']}"}
        order_data.update(new_note)
        return self.request.post('/orders/createorder', order_data)

    def activate_saturday_delivery(self, order_id: int):
         
        order_data = self.get_by_id(order_id=order_id).json()['orders'][0]
        sat_delivery = {"saturdayDelivery": sat_delivery}
        order_data.update(sat_delivery)
        return self.request.post('/orders/createorder', order_data)

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