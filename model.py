from pydantic import BaseModel, Field, field_validator, model_validator, computed_field, ConfigDict

from typing import Optional,Literal
# BaseModel check the input which user are provide is correct or not

class Model(BaseModel):
    # Configuration tool used for extra validation check
    model_config= ConfigDict(
        extra='forbid',  # decide create or not extra field
        frozen=True,      # Frozen Model means model me change nhi kr skte
        strict=True,       # pydantic khud se koi kam nhi krega agr isko False kr dete h to suppose if we are send id in string like "20" then pydantic will automaticaly convert inot int formate
        validate_assignment= True     # Validate on Edit
    )



    #data        : DataType
    id           :  int = Field(...,discreption="Item_Id") # Requried Field
    name         : str = Field(...,min_length=3,max_length=50 ,discreption="Item_Name")  # Required Field
    price        : float = Field(...,ge=0,discreption="Item_Price")  # Required Fiedl
    category     : Literal['Tea']
    is_availabel : bool   =Field(default=True,discreption="Item_Availability")  # Default Field assign used default inside Field
    discreption  : Optional[str] = None     # Optional Field

    # some special data type
    # email      : EmailStr   ->check input email is valid or not  ..... from pydantic import EmailStr
    # url        : AnyUrl     ->check input URL is valid or not   ...... from pydantic import AnyUrl
    # Date       : date       ->check valid date formate follow or not ..... from datetime import date
    




    # FieldValidator are used for perform operation on single field
    @field_validator('name') # only work on single field do not work on more then one field
    @classmethod
    def title_name(cls,value):
        return value.title()

    # Model Validator are work on multiple field
    @model_validator(mode='after')
    def check_availabel(self):
        if self.is_availabel and self.price<=0:
            raise ValueError('Available Item must have a price is greater then 0')
        return self


    # computed Field used for creating new field using old field
    @computed_field
    @property
    def price_tax(self) -> float:
        return round(self.price * 1.05, 2)

item=Model(rate=24,id=10,name="TEA",category='Tea',price=20,is_availabel=True,discreption="Good Tea")
print("data into normal Obj. Formate")
print(item)



#...................IN Serilization..................................
# jb bhi apne data ko kisi or function ko dena hota h do direct object ki form me nhi dete 
# yha item object ke form me data ko return kr rha h mtlb item ka datatype abhi object h

# .model_dump() -> are used for converting object data into dictionary formate
# this will work inside Python
print("Python ke arround send into dictonary form")
print(item.model_dump()) # this will given data into dictionary form not gives into object formate

#...................OUT Serilization..................................
# python ke around. inside python data send krna hota h tb dictonary use lete h
# over the internet/ over the website ya out of python data send krna hota h tb data json text file me send krte h 
print("Over the internet send into JSON txt")
print(item.model_dump_json())