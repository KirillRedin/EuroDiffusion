from city import City


class Country:
    def __init__(self, name, xl, yl, xh, yh):
        self.name = name
        self.cities = []
        self.neighbors = []
        self.complete_day = 0

        for i in range (xl, xh + 1):
            for j in range (yl, yh + 1):
                city = City(i, j, self.name)
                self.cities.append(city)

    def is_complete(self, countries_amount, complete_day):
        for city in self.cities:

            if len(city.coins_table) != countries_amount:
                return False

        if self.complete_day == 0:
            self.complete_day = complete_day

        return True

    def apply_changes(self):
        for city in self.cities:
            city.apply_changes()

    def fill_neighbors(self, grid, countries):
        coords = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        neighbors_names = []

        for city in self.cities:
            for coord in coords:
                try:
                    neighbor = grid[city.x + coord[0]][city.y + coord[1]]
                    if neighbor != 0:
                        if neighbor.country_name != self.name:
                            neighbors_names.append(neighbor.country_name)
                except IndexError:
                    continue

        for country in countries:
            for name in neighbors_names:
                if country.name == name:
                    self.neighbors.append(country)


