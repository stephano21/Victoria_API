import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Leer el conjunto de datos desde el archivo Excel
df = pd.read_excel('dataset.xlsx')

# Visualizar relaciones entre las variables mediante un pairplot
#sns.pairplot(df, diag_kind='kde')
#plt.show()
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.show()

