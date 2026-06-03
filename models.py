class ConnectionType:
    #represent typr of connector of charging station
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __str__(self):
        return f"{self.title}"

class Operator:
#represent the company that operator the charging station
    def __init__(self, id, title, website=None):
        self.id =id
        self.title=title
        self.website=website
    #website is optional

    def __str__(self):
        return f"{self.title}"

class Station:
    #represent single EV charging station
    def __init__(self, id, name, city, country, latitude, longitude, operator,connection_types, is_operational, number_of_points):
        self.id = id
        self.name =name
        self.city = city
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.operator = operator
        self.connection_types = connection_types
        #is working or not
        self.is_operational = is_operational
        #how many charging points available at the station
        self.number_of_points = number_of_points
    
    def __str__(self):
        status ="operational" if self.is_operational else "not operational"
        return f"{self.name} || {self.city}, {self.country} || {status} || {self.number_of_points} points"