class Ticker:

    def __init__(self, code, name, country, exchange, currency, type):
        self.code = code
        self.name = name
        self.country = country
        self.exchange = exchange
        self.currency = currency
        self.type = type

    @classmethod
    def from_dict(cls, data):
        mapping = {
            'Code': 'code',
            'Name': 'name',
            'Country': 'country',
            'Exchange': 'exchange',
            'Currency': 'currency',
            'Type': 'type',
        }
        filtered_data = {new_key: data.get(old_key, '') for old_key, new_key in mapping.items()}

        return cls(**filtered_data)
    
    @classmethod
    def to_dict(self):
        return {
            "name": self.code,
            "name": self.name,
            "country": self.country,
            "exchange": self.exchange,
            "currency": self.currency,
            "type": self.type,
        } 