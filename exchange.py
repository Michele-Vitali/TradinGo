class Exchange:

    def __init__(self, name, code, country, currency, countryISO2, countryISO3, operatingMIC):
        self.name = name
        self.code = code
        self.country = country
        self.currency = currency
        self.countryISO2 = countryISO2
        self.countryISO3 = countryISO3
        self.operatingMIC = operatingMIC
    
    @classmethod
    def from_dict(cls, data):
        mapping = {
            'Name': 'name',
            'Code': 'code',
            'Country': 'country',
            'Currency': 'currency',
            'CountryISO2': 'countryISO2',
            'CountryISO3': 'countryISO3',
            'OperatingMIC': 'operatingMIC'
        }
        filtered_data = {new_key: data.get(old_key, '') for old_key, new_key in mapping.items()}

        return cls(**filtered_data)
    
    @classmethod
    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code,
            "country": self.country,
            "currency": self.currency,
            "countryISO2": self.countryISO2,
            "countryISO3": self.countryISO3,
            "operatingMIC": self.operatingMIC
        }