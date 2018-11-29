import numpy
from country import Country
from city import City


class EuroDiffusion:
    def __init__(self):
        self.grid = []
        self.countries = []
        self.errors = []
        self.cases_count = 0
        self.countries_amount = 0
        self.days = 0
        self.case_is_correct = True
        self.grid_length, self.grid_height = 0, 0

    def parse(self, name):
        file = open(name, 'r')
        country_number = 0
        case_is_started = False

        for line in file:
            if case_is_started:
                country_number += 1

                if self.case_is_correct:
                    args = line.split()

                    if self.line_is_correct(args):
                        xl, yl, xh, yh = int(args[1]), int(args[2]), int(args[3]), int(args[4])
                        country = Country(args[0], xl, yl, xh, yh)
                        self.grid_length = max(self.grid_length, xl + 1, xh + 1)
                        self.grid_height = max(self.grid_height, yl + 1, yh + 1)
                        self.countries.append(country)

                if country_number == self.countries_amount:
                    case_is_started = False

            else:
                if self.cases_count > 0:
                    if self.case_is_correct:
                        self.fill_grid()
                        if self.case_is_correct:
                            self.count_days()
                    self.print_results()
                    self.clear_variables()

                try:
                    country_number = 0
                    self.cases_count += 1
                    self.countries_amount = int(line)
                    case_is_started = True

                except ValueError:
                    self.errors.append({'case': self.cases_count, 'text': 'UNEXPECTED VALUE'})
                    self.case_is_correct = False

    def line_is_correct(self, args):
        if len(args) != 5:
            self.errors.append({'case': self.cases_count, 'text': 'ARGS AMOUNT ERROR'})
            self.case_is_correct = False
            return False
        else:
            if not args[0].isalpha():
                self.errors.append({'case': self.cases_count,
                                    'text': 'COUNTRY NAME MUST INCLUDE ONLY ALPHABETIC CHARACTERS'})
                self.case_is_correct = False
                return False

            for i in range(1, 5):
                try:
                    if int(args[i]) < 0:
                        self.errors.append({'case': self.cases_count, 'text': 'COORDINATE CANNOT BE NEGATIVE NUMBER'})
                        self.case_is_correct = False
                        return False
                except ValueError:
                    self.errors.append({'case': self.cases_count, 'text': 'UNEXPECTED ARGUMENT VALUE'})
                    self.case_is_correct = False
                    return False
        return True

    def count_days(self):
        while not self.is_complete():
            self.days += 1

            for i in range(self.grid_length):
                for j in range(self.grid_height):
                    current_city = self.grid[i][j]

                    if current_city != 0:
                        neighbors = self.get_neighbors(i, j)
                        self.grid[i][j].transport_coins(neighbors)

            for country in self.countries:
                country.apply_changes()

    def countries_are_connected(self):
        for country in self.countries:
            if not self.is_connected(country):
                return False
            else:
                return True

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

    def is_complete(self):
        result = True
        for country in self.countries:
            result = country.is_complete(self.countries_amount, self.days) and result

        return result

    def fill_grid(self):
        for i in range(self.grid_length):
            cities = []

            for j in range(self.grid_height):
                cities.append(0)
            self.grid.append(cities)

        for country in self.countries:
            for city in country.cities:
                if self.grid[city.x][city.y] == 0:
                    self.grid[city.x][city.y] = city
                else:
                    self.errors.append({'case': self.cases_count,
                                        'text': 'MULTIPLE CITIES CAN NOT HAVE SAME COORDINATES'})
                    self.case_is_correct = False
                    return

        if not self.countries_are_connected():
            self.errors.append({'case': self.cases_count, 'text': 'COUNTRIES ARE NOT CONNECTED'})
            self.case_is_correct = False


    def print_grid(self):
        for i in range(self.grid_length):
            for j in range(self.grid_height):
                current_city = self.grid[i][j]

                if current_city != 0:
                    print('(', end=' ')

                    for coins in current_city.coins_table:
                        print(coins['country_name'], coins['amount'], end=' ')
                    print(')', end=' ')

            print()

    def clear_variables(self):
        self.grid = []
        self.countries = []
        self.countries_amount = 0
        self.days = 0
        self.grid_length, self.grid_height = 0, 0
        self.case_is_correct = True

    def print_results(self):
        print('Case %d' % self.cases_count)

        if self.case_is_correct:
            countries = sorted(self.countries, key=lambda country: country.complete_day)

            for country in countries:
                print(country.name, country.complete_day)
        else:
            for error in self.errors:
                if error['case'] == self.cases_count:
                    print('ERROR: %s' % error['text'])

        print()


diffusion_counter = EuroDiffusion()
diffusion_counter.parse('test3')
