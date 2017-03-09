import json
from pprint import pprint

class DataGathering:
	""" Class that gathers data from various data sources 
		TODO: EXPLICAR LA CLASE
		
	"""

	# def __init__(self):
		# self.twitter_data = False
		# self.select2 = False 
		# self.select3 = False
		# self.select4 = False
		# self.data    = []

	def getAEEData(self, key_1):
		""" 
			Funtion that reads a json file with energy related data and
			converts it into a format which can be readable by NVD3
			stacked chart. 

			Args:
				key_1 (str): The value for which we want to gather data.
				             This value comes from the energy.html file.

			Returns: 
				list: Contains 6 dictionaries. Each dictionary has a 
				key value (key_2 variable) and a value (values variable). 
				If an error occurs returns an empty array.
		"""

		# Variables
		suma         = 0  # Accumalator that holds the amount of data per year
		fiscal_year  = [] # Stores the year and the average amount of data per year
		values       = [] # Stores the fiscal year array for each key area
		result       = {} # Stores the value array and the key 2 variable
		final_result = [] # Stores the arrays of result
		
		try: 
			# Read energy related data and storing it in a dictionary
			with open('data/energy/AEE_SerieHistorica_2015.json') as data_file:
				energy_data = json.load(data_file)

			# Iterating through the file and storing the result
			for key_2 in energy_data[key_1]:
				for year in energy_data[key_1][key_2]:
					for month in energy_data[key_1][key_2][year]:
						suma +=energy_data[key_1][key_2][year][month]
					fiscal_year.append(year)
					fiscal_year.append(suma/12)
					values.append(fiscal_year)
					fiscal_year = []
					suma = 0
				result["key"] = key_2
				result["values"] = sorted(values)
				values = []
				final_result.append(result)
				result = {}
		except Exception as e:
			raise e
		finally:
			return final_result


# if __name__ == '__main__':
# 	data = DataGathering()
# 	pprint(data.getAEEData("Active Customers by Service Class"))
