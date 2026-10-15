from pydantic import BaseModel, Field, field_validator, model_validator,computed_field, ConfigDict, EmailStr, AnyUrl
from typing import Optional, Literal
from datetime import date

class Category(BaseModel): #Pydantic Model
    name: Literal['starter','main course', 'desert', 'beverage']


class Model(BaseModel):
    model_config = ConfigDict(
        extra  = 'allow',                #Extra Fields
        frozen = True   ,                #Frozen Model
        strict = True   ,                #Strict Pydantic Model     
        validate_assignment = True       #Validate on Edit
    )

    id           :   int
    name         :   str             = Field(...,min_length=3,max_length=50, description="Item name", alias='ItemName') 
    price        :   float           = Field(...,gt=0,description="Item price") 
    category     :   Category        = Field(...,description="Item category")
    is_available :   bool            = Field(default=True) 
    description  :   Optional[str]   = None
    # email        : EmailStr   -> valid email
    # url          : AnyUrl     -> Valid URL
    # Date         : date       -> Valid date format follow



    #Field Validator
    @field_validator('name')
    @classmethod
    def title_name(cls,value):
        return value.title()

    #Model Validator
    @model_validator(mode='after')
    def check_available(self):
        if self.is_available and self.price <= 0:
            raise('Available item must have price greater than 0')
        return self

    #ComputedField
    @computed_field
    @property
    def price_tax(self) -> float:
        return round(self.price * 1.05, 2)



item = Model(id=2, ItemName='Chole Kulche',price=10,category=Category(name='desert'), spicy = "Bohot tezz")

print('Dictionary model_dump()')
print(item.model_dump())

print('JSON model_dump_json()')
print(item.model_dump_json())




