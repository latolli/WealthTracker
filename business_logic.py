class BusinessLogic:
    def __init__(self, data_handler):
        self.data_handler = data_handler

    def calculate_total_wealth(self, month_data):
        total_assets = sum(month_data['assets'].values())
        loans = month_data['mortage_loan'] + month_data['other_loan']
        return total_assets - loans

    def prepare_data_for_plotting(self):
        data = self.data_handler.read_data()["monthly_data"]
        wealth_data = []
        income_data = []
        expenses_data = []
        expense_types_data = {
            "invested_and_loans_payed": [],
            "living_and_bills": [],
            "food_expenses": [],
            "sport_culture_travel": [],
            "other_expenses": []
        }
        months = []

        for entry in data:
            months.append(entry['month'])
            wealth_data.append(self.calculate_total_wealth(entry))
            income_data.append(entry['salary'] + entry['other_income'])
            total_expenses = (
                entry['invested_and_loans_payed'] +
                entry['living_and_bills'] +
                entry['food_expenses'] +
                entry['sport_culture_travel'] +
                entry['other_expenses']
            )
            expenses_data.append(total_expenses)

            for expense_type in expense_types_data.keys():
                expense_types_data[expense_type].append(entry[expense_type])

        return months, wealth_data, income_data, expenses_data, expense_types_data
    
    def prepare_assets_data_for_plotting(self):
        data = self.data_handler.read_data()["monthly_data"]
        assets_data = {
            "house": [],
            "investments": [],
            "bank": [],
            "car": []
        }
        months = []

        for entry in data:
            months.append(entry['month'])
            assets_data["house"].append(entry['assets']['house'] - entry['mortage_loan'])
            assets_data["car"].append(entry['assets']['car'])
            assets_data["bank"].append(entry['assets']['bank'] - entry['other_loan'])
            assets_data["investments"].append(entry['assets']['investments'])

        return months, assets_data
