import json
import os

# Specify the directory where your JSON files are located
input_directory = r'./Looperman_Loops/'

# Specify the output file where you want to save the combined JSON data
output_file = r'./meta.json'

# Create an empty list to store the combined JSON data
combined_data = dict()

# Loop through each JSON file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(input_directory, filename)
        with open(file_path, 'r') as file:
            # Load the JSON data from the file and append it to the combined_data list
            data = json.load(file)
            name = filename.split('_')[0]
            combined_data[name] = data

# Write the combined JSON data to the output file
with open(output_file, 'w') as output:
    json.dump(combined_data, output, indent=4)

print(f"Combined JSON data saved to {output_file}")