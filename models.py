# Property class
# Defines all proprties on the website and their details

# this library is used to declare the date and time of when this property is published on the website
from datetime import datetime

class Property:
    def __init__(self, prop_id, title, price, area, prop_type, bedrooms, bathrooms, image_url):
        self.prop_id = prop_id
        self.title = title
        self.price = price
        self.area = area
        self.prop_type = prop_type
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.image_url = image_url
        self.listed_at = datetime.now().isoformat()

    def to_dict(self):
        # this step for converting the property list to a json format
        return {
            'prop_id': self.prop_id,
            'title': self.title,
            'price': self.price,
            'area': self.area,
            'prop_type': self.prop_type,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'image_url': self.image_url,
            'listed_at': self.listed_at
        }
    
    def get_summary(self):
        # short summary of each property 
        return f"{self.bedrooms} bed {self.bathrooms} bath in {self.area} for EGP {self.price:,}!"

    def matches_filter(self, area=None, prop_type=None, max_price=None):
        # this function is used to filter the properties based on the user's search 
        if area and self.area != area:
            return False
        if prop_type and self.prop_type != prop_type:
            return False
        if max_price and self.price > max_price:
            return False
        return True
        if filters.get('max_price') and self.price > filters['max_price']:
            return False
        if filters.get('bedrooms') and self.bedrooms != filters['bedrooms']:
            return False
        if filters.get('bathrooms') and self.bathrooms != filters['bathrooms']:
            return False
        return True