"""
Ames Housing Dataset Visualization
====================================
"""
# sphinx_gallery_thumbnail_number = 3
from dabl import plot
from dabl.datasets import load_ames
import matplotlib.pyplot as plt

# load the ames housing dataset
# returns a plain dataframe
data = load_ames()



"""plot(data, 'SalePrice')
plt.show()"""
# Examine the first few rows of the dataset
print("\nFirst few rows of the dataset:")
print(data.head())

# Get information about the dataset structure
print("\nDataset information:")
print(data.info())

# Check for missing values
print("\nMissing values in each column:")
print(data.isnull().sum())

# Calculate and display missing value rates
missing_rates = (data.isnull().sum() / len(data)) * 100
missing_cols = missing_rates[missing_rates > 0].sort_values(ascending=False)

print("\nColumns with missing values and their missing rates (%):")
print(missing_cols)

# Separate numerical and categorical columns
numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = data.select_dtypes(include=['object']).columns

# Handle missing values in numerical columns
for col in numerical_cols:
    if data[col].isnull().sum() > 0:
        if col == 'LotFrontage':
            # Fill LotFrontage based on neighborhood median
            data[col] = data.groupby('Neighborhood')['LotFrontage'].transform(
                lambda x: x.fillna(x.median()))
        else:
            # Fill other numerical columns with median
            data[col].fillna(data[col].median(), inplace=True)

# Handle missing values in categorical columns
for col in categorical_cols:
    if data[col].isnull().sum() > 0:
        # Create a 'Missing' category for columns with high missing rates (>5%)
        if missing_rates[col] > 5:
            data[col].fillna('Missing', inplace=True)
        else:
            # Fill with mode for columns with low missing rates
            data[col].fillna(data[col].mode()[0], inplace=True)

# Verify no missing values remain
remaining_missing = data.isnull().sum().sum()
print(f"\nRemaining missing values: {remaining_missing}")
