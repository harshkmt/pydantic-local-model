from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict



class Model(BaseModel):

    model_config=ConfigDict(
        extra='forbid',
        strict=True,
        validate_assignment=True
    )

    email            : str = Field(..., description="E-MAIL")
    password         : str = Field(..., description="PASSWORD")
    conform_password : str = Field(..., description="CONFORM_PASSEORD")
    username         : str = Field(..., description="USERNAME", min_length=3, max_length=50)
    age              : int = Field(..., description="AGE", ge=18)





    # add field validator on email and username then we are convert all string letter in lowercase
    @field_validator('email')
    @classmethod
    def email_lowercase(cls,value):
        return value.lower()

    @field_validator('username')
    @classmethod
    def username_lowercase(cls,value):
        return value.lower()


    #add model validator for the verify passowerd and conform_password are same or not
    @model_validator(mode='after')
    def pass_verification(self):
        if len(self.password)<8:
            raise ValueError("Passeord must be 8 character")
        if self.password != self.conform_password:
            raise ValueError("conform_passeord are not same as a password")
         


user1 = Model(username="Harsh07", password="Harsh@123", conform_password="Harsh@123", email='HARSH@gmail.com', age=18)
print("user 1 details for creating account :")
for i in user1:
    print(i)



# in serlization
print("IN Serlization")
print(user1.model_dump())  # given output in dictionary

# out serlizatioln
print("OUT Serlization")
print(user1.model_dump_json())  # given output in JSON txt 