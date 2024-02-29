## Description:
This Python package serves as a comprehensive wrapper for the ShipStation API, designed to simplify the integration of ShipStation's shipping, fulfillment, and order management functionalities into your Python applications. By abstracting the complexities of direct API calls, this wrapper provides an intuitive interface for developers to interact with ShipStation, making it easier to automate shipping operations, manage orders, and streamline logistics processes directly from Python code.

## Features

- **Easy Configuration**: Set up your API keys once, and you're ready to interact with all available endpoints.
- **Order Management**: Retrieve, filter, and manage orders with simple method calls.
- **Shipment Handling**: List and update shipment details effortlessly.
- **Customer Insights**: Access and manage customer information, including filtering by specific criteria.
- **Customs Declarations**: Simplify international shipping with easy customs declaration updates.
- **Tag Management**: Apply tags to orders for easy organization and tracking.
- **Comprehensive Filters**: Utilize built-in filtering to easily manage and search through orders and shipments based on custom criteria.

## Installation:

Install the package using pip:

```bash
pip install shipstation-api-wrapper
```

## Getting Started: 

```python
from shipstation_api_wrapper.api import ShipStationClient

api_key = 'your_api_key_here'
client = ShipStationClient(api_key)

```

## Basic Usage: 

### Orders
- Retrieve an order by ID: 

```py
order = client.orders.get_by_id(order_id="123456")
print(order.json())
```

- List orders with custom filtering
```py
from shipstation_api_wrapper.filter import ShipStationOrderFilter

order_filter = ShipStationOrderFilter()
order_filter.add_order_number("1001")
orders = client.orders.list_with_filter(order_filter=order_filter)
print(orders.json())
```

## Advanced Features
Refer to the ShipStation API Documentation for more details on the advanced usage of the API.

## Contributing
I welcome contributions from the community! Please refer to the project's contributing guidelines for more information.
