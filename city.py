import copy


class City:
    def __init__(self, x, y, country_name):
        self.country_name = country_name
        self.x = x
        self.y = y
        self.coins_table = [{'country_name': country_name, 'amount': 1000000}]
        self.temp_table = [{'country_name': country_name, 'amount': 0}]

    def transport_coins(self, neighbors):
        for i in range(len(self.coins_table)):
            if self.coins_table[i]['amount'] >= 1000:
                portion = self.coins_table[i]['amount'] // 1000

                for neighbor in neighbors:
                    neighbor.add_coins(self.coins_table[i]['country_name'], portion)

                self.temp_table[i]['amount'] -= portion * len(neighbors)

    def add_coins(self, country_name, amount):
        for coins in self.temp_table:
            if coins['country_name'] == country_name:
                coins['amount'] += amount
                return

        self.temp_table.append({'country_name': country_name, 'amount': amount})

    def apply_changes(self):
        for i in range(len(self.temp_table)):
            try:
                self.coins_table[i]['amount'] += self.temp_table[i]['amount']
                self.temp_table[i]['amount'] = 0
            except IndexError:
                self.coins_table.append(copy.deepcopy(self.temp_table[i]))
                self.temp_table[i]['amount'] = 0
