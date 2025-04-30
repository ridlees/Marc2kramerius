import pandas as pd


Marc = pd.read_csv('q.csv')  
Kramerius = pd.read_csv('NDK.csv')

keys = ['Rok', 'Cislo', 'Strana']

Marc['101'] = Marc['101'].astype(str)


print(f"Marc {len(Marc)}")
print(f"Kramerius {len(Kramerius)}")
        
output = pd.merge(Marc, Kramerius, on=keys, how='inner')
print(f"Merged rows: {len(output)}")
output.to_csv('vysledek.csv') 

print("Merge complete. Output saved to 'merged_output.csv'.")
