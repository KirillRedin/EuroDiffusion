import copy


class City:
    def __init__(self, x, y, country_name):
        self.country_name = country_name
        self.x = x
        self.y = y
        self.neighbors = []
        self.coins_table = [{'country_name': country_name, 'amount': 1000000}]
        self.temp_table = [{'country_name': country_name, 'amount': 0}]

    def prepare_coins(self):
        for i in range(len(self.coins_table)):
            if self.coins_table[i]['amount'] >= 1000:
                # For each coin in country which amount >= 1000 get the portion to transport
                portion = self.coins_table[i]['amount'] // 1000

                for neighbor in self.neighbors:
                    # Prepare portion of coins to every neighbor
                    neighbor.add_coins(self.coins_table[i]['country_name'], portion)

                # Prepare portion of coins to take from city (portion to take = portion * amount of neighbors)
                self.temp_table[i]['amount'] -= portion * len(self.neighbors)

    def add_coins(self, country_name, amount):
        for coins in self.temp_table:
            # Check if city already has coins of this country
            if coins['country_name'] == country_name:
                # Prepare amount of coins from other country to add
                coins['amount'] += amount
                return

        # If temporary table does not contain coins of this country, append them
        self.temp_table.append({'country_name': country_name, 'amount': amount})

    def transport_coins(self):
        for i in range(len(self.temp_table)):
            try:
                # Transport coins from temporary table
                self.coins_table[i]['amount'] += self.temp_table[i]['amount']

            except IndexError:
                # If temporary table contains coins from a new country, append them to the main table
                self.coins_table.append(copy.deepcopy(self.temp_table[i]))

            # Reset temporary value
            self.temp_table[i]['amount'] = 0

    def fill_neighbors(self, grid):
        # Coordinates of possible neighbors
        coords = [[-1, 0], [0, -1], [1, 0], [0, 1]]
        for coord in coords:
            try:
                # Check if current city has neighbors and add them to list
                if grid[self.x + coord[0]][self.y + coord[1]] != 0:
                    self.neighbors.append(grid[self.x + coord[0]][self.y + coord[1]])
            except IndexError:
                continue
