from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Optional, Union

class Address(BaseModel):
    name: Optional[str]
    company: Optional[str]
    street1: Optional[str]
    street2: Optional[str]
    street3: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postalCode: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    residential: Optional[bool]
    addressVerified: Optional[str] = Field(None, description="Read-Only")

class AdvancedOptions(BaseModel):
    warehouseId: Optional[int] = None
    nonMachinable: bool
    saturdayDelivery: bool
    containsAlcohol: bool
    storeId: int
    customField1: Optional[str] = None
    customField2: Optional[str] = None
    customField3: Optional[str] = None
    source: Optional[str] = None
    mergedOrSplit: bool = Field(None, description="Read-Only")
    mergedIds: List[int] = Field(None, description="Read-Only")
    parentId: Optional[int] = None
    billToParty: Optional[str] = None
    billToAccount: Optional[str] = None
    billToPostalCode: Optional[str] = None
    billToCountryCode: Optional[str] = None
    billToMyOtherAccount: Optional[str] = None

class CustomsItem(BaseModel):
    customsItemId: Optional[int] = Field(93985654, description="Read-Only")
    description: str
    quantity: int=1
    value: float
    harmonizedTariffCode: str="821500"
    countryOfOrigin: str="US"

class Dimensions(BaseModel):
    length: float
    width: float
    height: float
    units: str

class InsuranceOptions(BaseModel):
    provider: str
    insureShipment: bool
    insuredValue: float

class InternationalOptions(BaseModel):
    contents: str
    customsItems: List[CustomsItem]
    nonDelivery: str

class ItemOption(BaseModel):
    name: str
    value: str

class OrderItem(BaseModel):
    orderItemId: int = Field(..., description="Read-Only")
    lineItemKey: str
    sku: str
    name: str
    imageUrl: str
    weight: 'Weight'  # This will be defined later
    quantity: int
    unitPrice: float
    taxAmount: float
    shippingAmount: float
    warehouseLocation: Optional[str] = None
    options: List[ItemOption]
    productId: int
    fulfillmentSku: Optional[str]
    adjustment: bool
    upc: Optional[str]
    createDate: Optional[str] = Field(..., description="Read-Only")
    modifyDate: Optional[str] = Field(..., description="Read-Only")

class Weight(BaseModel):
    value: float
    units: str
    WeightUnits: int = Field(..., description="Read-Only")

class Order(BaseModel):
    orderId: int = Field(..., description="Read-Only")
    orderNumber: str
    orderKey: str
    orderDate: str
    createDate: str = Field(..., description="Read-Only")
    modifyDate: str = Field(..., description="Read-Only")
    paymentDate: str
    shipByDate: str
    orderStatus: str
    customerId: int = Field(..., description="Read-Only")
    customerUsername: str
    customerEmail: str
    billTo: Address
    shipTo: Address
    items: List[OrderItem]
    orderTotal: float = Field(..., description="Read-Only")
    amountPaid: float
    taxAmount: float
    shippingAmount: float
    customerNotes: Optional[str]
    internalNotes: Optional[str]
    gift: bool
    giftMessage: Optional[str]
    paymentMethod: Optional[str]
    requestedShippingService: Optional[Optional[str]] = None
    carrierCode: Optional[str]
    serviceCode: Optional[str]
    packageCode: Optional[str]
    confirmation: Optional[str]
    shipDate: Optional[str]
    holdUntilDate: Optional[str] = None
    weight: Weight
    dimensions: Dimensions
    insuranceOptions: InsuranceOptions
    internationalOptions: InternationalOptions
    advancedOptions: AdvancedOptions
    tagIds: Optional[List[int]] = None
    userId: str = Field(..., description="Read-Only")
    externallyFulfilled: bool = Field(..., description="Read-Only")
    externallyFulfilledBy: Optional[str] = Field(None, description="Read-Only")
    
    @field_validator('internationalOptions')
    def validate_international_options(cls, v):
        if v is None:
            return {"customsItems": []}
        return v
    
OrderItem.model_rebuild()
