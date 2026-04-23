# Property class
# Defines all proprties on the website and their details

# this library is used to declare the date and time of when this property is published on the website
from datetime import datetime

class Property:
    def __init__(self, id, title, area, description, price, location, image_url, bedrooms, bathrooms):
        self.id = id
        self.title = title
        self.area = area
        self.description = description
        self.price = price
        self.location = location
        self.image_url = image_url
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.listed_at = datetime.now().isoformat()

    def to_dict(self):
        # this step for converting the property list to a json format
        return {
            'id': self.id,
            'title': self.title,
            'area': self.area,
            'description': self.description,
            'price': self.price,
            'location': self.location,
            'image_url': self.image_url,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'listed_at': self.listed_at
        }
    
    def propSummary(self):
        # short summary of each property 
        return f"{self.bedrooms} bed {self.bathrooms} bath in {self.area} for EGP {self.price:,}"

    def matchFilters(self, filters):
        # this function is used to filter the properties based on the user's search 
        if filters.get('area') and self.area != filters['area']:
            return False
        if filters.get('min_price') and self.price < filters['min_price']:
            return False
        if filters.get('max_price') and self.price > filters['max_price']:
            return False
        if filters.get('bedrooms') and self.bedrooms != filters['bedrooms']:
            return False
        if filters.get('bathrooms') and self.bathrooms != filters['bathrooms']:
            return False
        return True