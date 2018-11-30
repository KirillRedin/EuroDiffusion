from city import City


class Country:
    def __init__(self, name, xl, yl, xh, yh):
        self.name = name
        self.cities = []
        self.neighbors = []
        self.complete_day = 0

        # Filling country cities
        for i in range(xl, xh + 1):
            for j in range(yl, yh + 1):
                city = City(i, j, self.name)
                self.cities.append(city)

    def is_complete(self, countries_amount, complete_day):
        for city in self.cities:
            # Check if amount of motifs in each city same as amount of countries
            if len(city.coins_table) != countries_amount:
                return False

        # Check if this country was completed earlier or not
        if self.complete_day == 0:
            self.complete_day = complete_day

        return True

    def transport_coins(self):
        for city in self.cities:
            city.transport_coins()

    def fill_neighbors(self, grid, countries):
        neighbors_names = []

        # Fill city neighbors
        for city in self.cities:
            city.fill_neighbors(grid)

        for city in self.cities:
            for neighbor in city.neighbors:
                # If country name of neighbor city is different, add it to neighbor country names list
                if neighbor.country_name != self.name:
                    neighbors_names.append(neighbor.country_name)

        # Get country neighbors by names from neighbor country names list
        for country in countries:
            for name in neighbors_names:
                if country.name == name:
                    self.neighbors.append(country)


