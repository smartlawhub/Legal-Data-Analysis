import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# Format dates
def clean_and_parse_date(date_str):
    date_str = date_str.split(';')[0]  
    return datetime.strptime(date_str, "%d/%m/%Y")

# Load the data
directives_df = pd.read_csv('directives.csv')
transposed_act_df = pd.read_csv('transposed_act.csv')

# Applying the function of format the date
directives_df['Date'] = directives_df['Date'].apply(clean_and_parse_date)
transposed_act_df['Date'] = transposed_act_df['Date'].apply(clean_and_parse_date)

# Group by celex and select the oldest occurence for calculation
transposed_min_dates = transposed_act_df.groupby(['Transposed act', 'Country'])['Date'].min().reset_index()

# Scoring
results = []
for _, row in transposed_min_dates.iterrows():
    transposed_celex = row['Transposed act']
    country = row['Country']
    transposed_date = row['Date']
    
    directive_row = directives_df[directives_df['CELEX'] == transposed_celex]
    
    if not directive_row.empty:
        directive_date = directive_row.iloc[0]['Date']
        subject = directive_row.iloc[0]['Subjects']  # Capture the subject from the directive row
        difference = (transposed_date - directive_date).days
        corrected_score = max(difference, 0)  # Corrected score: 0 if negativen otherwise keep the result
        
        results.append({
            'Transposed CELEX': transposed_celex,
            'Country': country,
            'Subject': subject,  # Include the subject in the results
            'Date Difference (Days)': difference,
            'Corrected Score': corrected_score
        })

# Create the dataframe for further analysis
results_df = pd.DataFrame(results)

print(results_df)

# Save in csv
results_df.to_csv('date_differences_with_subjects.csv', index=False)

# Calculate score for each country
country_scores = results_df.groupby('Country')['Corrected Score'].sum().reset_index()

# Rank countries
country_rankings = country_scores.sort_values(by='Corrected Score', ascending=True).reset_index(drop=True)
print("Delay of transposition by countries (days)")
print(country_rankings)

# Normalize score for color purpose in the graph
scores = country_rankings['Corrected Score']
normalized_scores = (scores - scores.min()) / (scores.max() - scores.min())

#color gradient by score
colors = [mcolors.to_rgba(c) for c in plt.cm.RdYlGn_r(np.linspace(0, 1, len(scores)))]
bar_colors = [colors[int(np.round(score * (len(colors) - 1)))] for score in normalized_scores]

plt.figure(figsize=(10, 6))
bars = plt.bar(country_rankings['Country'], country_rankings['Corrected Score'], color=bar_colors)

plt.xlabel('Country')
plt.ylabel('Corrected Score')
plt.title('Transposition delay (day)')

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# Group by countries and count transposed act
unique_transposed_counts = transposed_act_df.groupby('Country')['Transposed act'].nunique().reset_index()

unique_transposed_counts['Number of Transposed Acts'] = unique_transposed_counts['Transposed act']

unique_transposed_counts.drop(columns=['Transposed act'], inplace=True)


# Sort countries by acts transposed
unique_transposed_counts_sorted = unique_transposed_counts.sort_values(by='Number of Transposed Acts', ascending=False).reset_index(drop=True)
print("\nNumber of transposed acts")
print(unique_transposed_counts_sorted)

# Show subject by celex
celex_subjects = directives_df[['CELEX', 'Subjects']]
# Separate subject to have on a single row
subjects_expanded = directives_df.set_index('CELEX')['Subjects'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).reset_index(name='Subject')

print(subjects_expanded.head())
# Merge dataframe to get subject with country
merged_df = pd.merge(subjects_expanded, transposed_act_df, left_on='CELEX', right_on='Transposed act', how='inner')

# Get the number of celex by subject
subject_country_counts = merged_df.groupby(['Subject', 'Country']).size().reset_index(name='Count')

print(subject_country_counts.head())


# Today
today = pd.to_datetime('today')

# Get all celex
unique_celex = directives_df['CELEX'].unique()

# Get all countries
unique_countries = transposed_act_df['Country'].unique()

# List to collect results
results = []

# Non transposed celex
for country in unique_countries:
    transposed_celex_for_country = transposed_act_df[transposed_act_df['Country'] == country]['Transposed act'].unique()
    non_transposed_celex = [celex for celex in unique_celex if celex not in transposed_celex_for_country]
    
    # Calculate delay compared to today's date
    for celex in non_transposed_celex:
        directive_info = directives_df[directives_df['CELEX'] == celex]
        if not directive_info.empty:
            publication_date = pd.to_datetime(directive_info.iloc[0]['Date'])
            days_difference = (today - publication_date).days
            results.append({
                'Country': country,
                'CELEX': celex,
                'Days Since Publication': days_difference
            })

results_df = pd.DataFrame(results)
print(results_df)

results_df.to_csv('non_transposed_celex_by_country.csv', index=False)

# Split all subject into a dataframe
expanded_subjects_df = directives_df.drop('Subjects', axis=1).join(directives_df['Subjects'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True).rename('Subject'))

# count by country number of celex by subject
subject_country_transposed_counts = transposed_act_df.merge(expanded_subjects_df, left_on='Transposed act', right_on='CELEX').groupby(['Country', 'Subject']).size().reset_index(name='Unique Transposed Acts Count')

print("Number of acts transposed:")
print(subject_country_transposed_counts)

# Visualisation for a given country
selected_country = 'France'  
selected_data = subject_country_transposed_counts[subject_country_transposed_counts['Country'] == selected_country].sort_values(by='Unique Transposed Acts Count', ascending=False)

# counting
total_transposed_by_subject = subject_country_transposed_counts.groupby('Subject')['Unique Transposed Acts Count'].sum().reset_index()

# sorting
top_subjects = total_transposed_by_subject.sort_values(by='Unique Transposed Acts Count', ascending=False).head(10)

# first 10 subjects
plt.figure(figsize=(12, 8))
plt.bar(top_subjects['Subject'], top_subjects['Unique Transposed Acts Count'], color='skyblue')
plt.title('Top 10 Subjects by Number of Unique Transposed Acts for France')
plt.xlabel('Subject')
plt.ylabel('Number of Unique Transposed Acts')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# counting
subject_country_transposed_counts = transposed_act_df.merge(
    expanded_subjects_df, left_on='Transposed act', right_on='CELEX').groupby(['Subject']).size().reset_index(name='Unique Transposed Acts Count')

# sorting
sorted_subjects = subject_country_transposed_counts.sort_values(by='Unique Transposed Acts Count', ascending=False)

# ploting
plt.figure(figsize=(12, 8))
plt.bar(unique_transposed_counts_sorted['Country'], unique_transposed_counts_sorted['Number of Transposed Acts'], color='teal')
plt.title('Number of transposed act by country')
plt.xlabel('Country')
plt.ylabel('Number of acts')
plt.xticks(rotation=90)  # Rotation des étiquettes de l'axe des x pour une meilleure lisibilité
plt.tight_layout()
plt.show()

# selection of the top ten subjects
top_10_subjects = sorted_subjects.head(10)

print("Acts transposed by subject :")
print(sorted_subjects)

total_transposed_by_country = transposed_act_df.groupby('Country').size().reset_index(name='Total Transposed Acts')

sorted_countries_by_transposed_acts = total_transposed_by_country.sort_values(by='Total Transposed Acts', ascending=False)


