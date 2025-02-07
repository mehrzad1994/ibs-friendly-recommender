#import libraries
from pydantic import BaseModel, conlist, Field, ValidationError
from typing import Dict, List
import json



#food categories base model

class FoodCategory(BaseModel):
    fruit: list[str] = Field(default_factory=list)
    vegetable: list[str] = Field(default_factory=list)
    protein: list[str] = Field(default_factory=list)
    carbohydrates: list[str] = Field(default_factory=list)
    dairy: list[str] = Field(default_factory=list)
    nuts_and_seeds: list[str] = Field(default_factory=list)
    beverages: list[str] = Field(default_factory=list)
    alcohol: list[str] = Field(default_factory=list)
    condiment: list[str] = Field(default_factory=list)
    sweets: list[str] = Field(default_factory=list)
    herbs_and_spices: list[str] = Field(default_factory=list)
    legums: list[str] = Field(default_factory=list)


#food approval base model

class FoodApproval(BaseModel):
    approved_food: FoodCategory
    avoided_food: FoodCategory


# Defining a main class with methods for all functionalities

class FoodApprovalManager:
    def __init__(self, approved_food: FoodCategory = None, avoided_food: FoodCategory = None):
        self.food_approval = FoodApproval(
            approved_food=approved_food or FoodCategory(),
            avoided_food=avoided_food or FoodCategory()
        )

    @classmethod
    def from_json_file(cls, file_path: str):
        #Initialize the manager from a JSON file.
        with open(file_path, "r") as f:
            data = json.load(f)
        try:
            food_approval = FoodApproval.model_validate(data)
            return cls(approved_food=food_approval.approved_food, avoided_food=food_approval.avoided_food)
        except ValidationError as e:
            print("Validation error:", e)
            return None

    def to_json_file(self, file_path: str):
        #Save the current food approval data to a JSON file
        with open(file_path, "w") as f:
            json.dump(self.food_approval.model_dump(), f, indent=4)

    def get_approved_food(self) -> FoodCategory:
        #Return approved food categories
        return self.food_approval.approved_food

    def get_avoided_food(self) -> FoodCategory:
        #Return avoided food categories
        return self.food_approval.avoided_food

    def add_food(self, category: str, food: str, approved: bool = True):
        #Add a food item to a specific category
        target = self.food_approval.approved_food if approved else self.food_approval.avoided_food
        if hasattr(target, category):
            getattr(target, category).append(food)
        else:
            print(f"Category '{category}' does not exist.")

    def remove_food(self, category: str, food: str, approved: bool = True):
        #Remove a food item from a specific category
        target = self.food_approval.approved_food if approved else self.food_approval.avoided_food
        if hasattr(target, category):
            getattr(target, category).remove(food) if food in getattr(target, category) else print(f"{food} not found in {category}")
        else:
            print(f"Category '{category}' does not exist.")

            
    def search_food(self, food_name: str):
        # Search in approved food categories
        for category, foods in self.food_approval.approved_food.dict().items():
            if food_name in foods:
                return f"'{food_name}' found in approved foods under '{category}' category."

        # Search in avoided food categories
        for category, foods in self.food_approval.avoided_food.dict().items():
            if food_name in foods:
                return f"'{food_name}' found in avoided foods under '{category}' category."

        return f"'{food_name}' not found in any category."

    
    def search_food_int(self, food_name: str):
        # Search in approved food categories
        for category, foods in self.food_approval.approved_food.dict().items():
            if food_name in foods:
                return 1

        # Search in avoided food categories
        for category, foods in self.food_approval.avoided_food.dict().items():
            if food_name in foods:
                return -1

        return 0
