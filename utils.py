#functional programming /filder;map, lambda,decorators

def log_action(func):
    def wrapper(*args,**kwargs):
        print(f"-- {func.__name__} started--")
        result= func(*args,**kwargs)
        print(f"--{func.__name__} done--")
        return result
    return wrapper

#filter station by country
@log_action
def filter_by_country(stations, country):
    #filter just station in own country
    return list(filter(lambda s: s.country == country, stations))

#filter just operational stations
@log_action
def filter_operational(stations):
    return list(filter(lambda s: s.is_operational == True, stations))

#get all stations name
@log_action
def get_all_names(stations):
    return list(map(lambda s: s.name, stations))

#stations by number of points
@log_action
def sort_by_points(stations):
    return sorted(stations, key =lambda s: s.number_of_points or 0, reverse=True)


#analyse stations- statisctics
@log_action
def analyze_stations(stations):
    #calculate total stations
    total =len(stations)
    #calculate station operational
    operational = len(list(filter(lambda s: s.is_operational == True, stations)))

    #calculate total chargin points
    total_points = sum(map(lambda s: s.number_of_points or 0, stations))

    #dictionary with all statistics
    return{
        "total_stations": total,
        "operational_stations": operational,
        "non_operational_stations": total- operational,
        "total_charging_points": total_points,
    }