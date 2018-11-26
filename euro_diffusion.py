import numpy
from country import Country
from city import City


class EuroDiffusion:
    def __init__(self):
        self.grid = []
        self.transport_grid = []
        self.countries = []
        self.cases_count = 0
        self.countries_amount = 0
        self.days = 0
        self.largest_x, self.largest_y = 0, 0

    def parse(self, name):
        file = open(name, 'r')
        country_number = 0

        for line in file:

            if country_number < self.countries_amount:
                country_number += 1
                args = line.split()

                if len(args) != 5:
                    print('ARGS AMOUNT ERROR')
                else:
                    if not args[0].isalpha():
                        print("Country name must include only alphabetic characters")
                        return

                    for i in range(1, 4):
                        try:
                            int(args[i])
                        except ValueError:
                            print("UNEXPECTED ARGUMENT VALUE '%s'" % args[i])
                            return

                    country = Country(args[0], int(args[1]), int(args[2]), int(args[3]), int(args[4]))
                    self.countries.append(country)
                continue

            if self.cases_count > 0:
                self.fill_grid()
                for country in self.countries:
                    if not self.is_connected(country):
                        print('Case %d' % self.cases_count)
                        print('COUNTRIES ARE NOT CONNECTED!')
                        return
                self.count_days()
                self.print_results()
                self.clear_variables()

            try:
                country_number = 0
                self.cases_count += 1
                self.countries_amount = int(line)

            except ValueError:
                print('UNEXPECTED VALUE')
                return

    def count_days(self):
        while not self.is_complete():
            self.days += 1

            # print(self.days)
            # self.print_grid()

            for i in range(20):
                for j in range(20):
                    current_city = self.grid[i][j]

                    if current_city != 0:
                        neighbors = self.get_neighbors(i, j)
                        self.grid[i][j].transport_coins(neighbors)

            for country in self.countries:
                country.apply_changes()

        # print(self.days)
        # self.print_grid()

    def get_neighbors(self, x, y):
        coords = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        neighbors = []

        for coord in coords:
            try:
                if self.grid[x + coord[0]][y + coord[1]] != 0:
                    neighbors.append(self.grid[x + coord[0]][y + coord[1]])
            except IndexError:
                continue

        return neighbors

    def is_connected(self, country):
        coords = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        for city in country.cities:
            for coord in coords:
                try:
                    if self.grid[city.x + coord[0]][city.y + coord[1]] != 0:
                        if self.grid[city.x + coord[0]][city.y + coord[1]].country_name != country.name:
                            return True
                except IndexError:
                    continue

        return False

    def transport_coins(self, current_city, neighbors):
        neighbors_coins = []
        current_city_coins = []

        for coins in current_city.coins_table:

            transport_coins = {'country_name': coins['country_name'], 'amount': int(coins['amount'] / 1000)}
            neighbors_coins.append(transport_coins)

            transport_coins['amount'] *= -1 * len(neighbors)
            current_city_coins.append(transport_coins)

        for neighbor in neighbors:
            self.transport_grid[neighbor.x][neighbor.y] = neighbors_coins

    def is_complete(self):
        result = True
        for country in self.countries:
            result = country.is_complete(self.countries_amount, self.days) and result

        return result

    def fill_grid(self):
        for i in range(20):
            cities = []

            for j in range(20):
                cities.append(0)
            self.grid.append(cities)
            self.transport_grid.append(cities)

        for country in self.countries:
            for city in country.cities:
                if self.grid[city.y][city.x] == 0:
                    self.grid[city.y][city.x] = city
                else:
                    print("ERROR! WRONG COORDINATES WERE PROVIDED")

    def print_grid(self):
        for i in range(20):
            for j in range(20):
                current_city = self.grid[i][j]

                if current_city != 0:
                    print('(', end=' ')

                    for coins in current_city.coins_table:
                        print(coins['country_name'], coins['amount'], end=' ')

                    print(')', end=' ')
            print()

    def clear_variables(self):
        self.grid = []
        self.transport_grid = []
        self.countries = []
        self.countries_amount = 0
        self.days = 0
        self.largest_x, self.largest_y = 0, 0

    def print_results(self):
        countries = sorted(self.countries, key=lambda country: country.complete_day)
        print('Case %d' % self.cases_count)

        for country in countries:
            print(country.name, country.complete_day)

        print()


diffusion_counter = EuroDiffusion()
diffusion_counter.parse('test3')