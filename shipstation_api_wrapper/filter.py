from typing import Optional, Dict

class ShipStationOrderFilter:
    def __init__(self) -> None:
        self.params: Dict[str, str] = {}

    def add_customer_name_filter(self, customer_name: Optional[str] = None) -> None:
        if customer_name:
            self.params['customerName'] = customer_name

    def add_item_keyword_filter(self, item_keyword: Optional[str] = None) -> None:
        if item_keyword:
            self.params['itemKeyword'] = item_keyword

    def add_date_filter(self, start_date: Optional[str] = None, end_date: Optional[str] = None, date_type: str = 'create') -> None:
        if start_date:
            self.params[f'{date_type}DateStart'] = start_date
        if end_date:
            self.params[f'{date_type}DateEnd'] = end_date

    def add_order_status_filter(self, order_status: Optional[str] = None) -> None:
        statuses = ["awaiting_payment", "awaiting_shipment", "shipped", "on_hold", "cancelled"]
        assert order_status in statuses, f"Status Must be one of {statuses}"  
        if order_status:
            self.params['orderStatus'] = order_status

    def add_order_number(self, order_number:int): 
        if order_number:
            self.params['orderNumber'] = order_number
    
    def add_tag_filter(self, tag_id:int):
        if tag_id:
            self.params['tagId'] = tag_id

    def get_filters(self) -> Dict[str, str]:
        return self.params
    
class ShipStationProductFilter: 
    def __init__(self) -> None:
        self.params: Dict[str, str] = {}

    def add_sku_filter(self, sku: Optional[str] = None) -> None:
        if sku:
            self.params['sku'] = sku
        
    def get_filters(self) -> Dict[str, str]:
        return self.params