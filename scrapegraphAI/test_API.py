from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger
from typing import Any, List, Tuple, Dict
from pydantic import BaseModel, Field
import os
import csv
import json
import time

sgai_logger.set_logging(level="INFO")

# Initialize the client
sgai_client = Client(api_key="MYKEY")

# Define the schema
class PDPEcommerceSchema(BaseModel):
	ProductCode: str = Field(description="Unique code that describes the product")
	ProductFullPrice: float = Field(description="Full price of the product, before any discount applied. If there's no discount applied, it's the final product price")
	ProductFinalPrice: float = Field(description="The final sale price of the product, after discounts.")
	CurrencyCode: str = Field(description="ISO3 currency code")
	BrandName: str = Field(description="The name of the product's manufacturer")
	ProductUrl: str = Field(description="URL of the product page")
	MainImageURL: str = Field(description="URL of the main image of the product")
	ProductMainCategory: str = Field(description="The main category of the product, usually the first item of the breadcrumb")
	ProductSubcategory: str = Field(description="The product subcategory, usually the second level of the breadcrumb")

def read_urls_from_file(file_path: str) -> List[Tuple[str, str]]:
	"""Read URLs from a file with format 'number|URL'"""
	urls = []
	try:
		with open(file_path, 'r') as f:
			for line in f:
				line = line.strip()
				if line:
					parts = line.split('|', 1)  # Split only on the first '|'
					if len(parts) == 2:
						number, url = parts
						urls.append((number, url))
					else:
						print(f"Warning: Skipping malformed line: {line}")
	except FileNotFoundError:
		print(f"Error: File {file_path} not found.")
	except Exception as e:
		print(f"Error reading file: {e}")
	
	return urls

def save_result_to_json(result: Dict, number: str):
	"""Save a single result to a JSON file"""
	os.makedirs("results_json", exist_ok=True)
	json_filename = f"results_json/result_{number}.json"
	
	try:
		with open(json_filename, 'w', encoding='utf-8') as f:
			json.dump(result, f, indent=2, ensure_ascii=False)
		print(f"Saved JSON result to {json_filename}")
	except Exception as e:
		print(f"Error saving result to JSON: {e}")

def save_result_to_csv(result: Dict, output_file: str, create_new: bool = False):
	"""Save a single result to a CSV file"""
	# Define the exact column order as specified
	fieldnames = [
		'URLNumber', 
		'OriginalURL', 
		'ProductCode', 
		'ProductFullPrice', 
		'ProductFinalPrice', 
		'CurrencyCode', 
		'BrandName', 
		'ProductUrl', 
		'MainImageURL', 
		'ProductMainCategory', 
		'ProductSubcategory'
	]
	
	# Clean up result before writing to CSV
	for field in fieldnames:
		if field not in result:
			result[field] = ""
		elif result[field] is None:
			result[field] = ""
	
	try:
		mode = 'w' if create_new else 'a'
		file_exists = os.path.exists(output_file) and not create_new
		
		with open(output_file, mode, newline='', encoding='utf-8') as f:
			writer = csv.DictWriter(f, fieldnames=fieldnames)
			if mode == 'w' or not file_exists:
				writer.writeheader()
			writer.writerow(result)
		print(f"Updated CSV file: {output_file}")
	except Exception as e:
		print(f"Error saving result to CSV: {e}")

def process_urls(urls: List[Tuple[str, str]]):
	output_file = "output.csv"
	# Create a new CSV file with headers
	save_result_to_csv({}, output_file, create_new=True)
	
	for number, url in urls:
		print(f"\nProcessing #{number}: {url}")
		try:
			# SmartScraper request
			response = sgai_client.smartscraper(
				website_url=url,
				user_prompt="Extract the product info from this page",
				output_schema=PDPEcommerceSchema
			)
			
			# Print the response ID
			print(f"Request ID: {response['request_id']}")
			
			# Process the result
			if response.get('result'):
				result_data = response['result']
				# Add the URL number and original URL to the result
				result_data['URLNumber'] = number
				result_data['OriginalURL'] = url
				
				# Save the individual result to JSON
				save_result_to_json(result_data, number)
				
				# Append the result to the CSV file
				save_result_to_csv(result_data, output_file)
			
			# Still print reference URLs to console for debugging
			if response.get('reference_urls'):
				print(f"Reference URLs: {response['reference_urls']}")
				
		except Exception as e:
			print(f"Error processing URL {url}: {e}")
			# Save error entry to JSON and CSV
			error_data = {
				'URLNumber': number,
				'OriginalURL': url,
				'Error': str(e)
			}
			save_result_to_json(error_data, f"{number}_error")
			save_result_to_csv(error_data, output_file)

def main():
	input_file = "input.txt"
	urls = read_urls_from_file(input_file)
	
	if urls:
		print(f"Found {len(urls)} URLs to process")
		process_urls(urls)
	else:
		print("No valid URLs found in the input file.")
	
	# Close the client at the end
	sgai_client.close()

if __name__ == "__main__":
	main()