from bs4 import BeautifulSoup
import os
import re
import csv
import pandas as pd
import matplotlib.pyplot as plt

pattern = r'\((\d+)\)'
folder_1 = []
folder_2 = []
def extract_file(folder_path, storage_folder):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            file_name = os.path.join(root, file_name)
            storage_folder.append(file_name)

folder_path_1 = '/home/reddy/nandi/Energy Modeling Outputs/1'
folder_path_2 = '/home/reddy/nandi/Energy Modeling Outputs/2'
extract_file(folder_path_1, folder_1)
extract_file(folder_path_2, folder_2)

output_1 = '/home/reddy/nandi/Energy Modeling Outputs/output/1'
output_2 = '/home/reddy/nandi/Energy Modeling Outputs/output/2'

if not os.path.exists(output_1):
    os.makedirs(output_1)
if not os.path.exists(output_2):
    os.makedirs(output_2)

list_output_1 = []
list_output_2 = []
x_label = ['1.csv', '2.csv', '3.csv', '4.csv', '5.csv', '6.csv', '7.csv', '8.csv', '9.csv', '10.csv']
for i in x_label:
    list_output_1.append(os.path.join(output_1, i))
    list_output_2.append(os.path.join(output_2, i))


def extract_table(html_file, output_file):
    with open(html_file, 'r', encoding = 'utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', {'border': '1', 'cellpadding': '4', 'cellspacing': 0})
    data = []

    for row in table.find_all('tr'):
        columns = row.find_all('td')
        row_data = [col.text.strip() for col in columns]
        data.append(row_data)
    
    with open(output_file, 'w', newline='', encoding = 'utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        headers = data[0]
        csv_writer.writerow(headers)
        for row in data[1:]:
            csv_writer.writerow(row)

def draw_distribution_graph(list):
    values = []
    for file in list:
        df = pd.read_csv(file)
        values.append(df['Energy Per Conditioned Building Area [MJ/m2]'].iloc[0])
    
    plt.plot(x_label, values)
    plt.xlabel("csv")
    plt.ylabel("Total Site Energy")
    plt.title("Total Site Energy based on Energy per conditioned building area")
    plt.show()

for i in range(len(folder_1)):
    match = re.search(pattern, folder_1[i])
    output_file_name = os.path.join(output_1, '{}.csv'.format(match.group(1)))
    extract_table(folder_1[i], output_file_name)

for i in range(len(folder_2)):
    match = re.search(pattern, folder_2[i])
    output_file_name = os.path.join(output_2, '{}.csv'.format(match.group(1)))
    extract_table(folder_2[i],  output_file_name)

draw_distribution_graph(list_output_1)
draw_distribution_graph(list_output_2)