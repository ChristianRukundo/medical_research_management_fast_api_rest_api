import requests
import pandas as pd


def fetch_data_from_endpoint_paginated(endpoint_url, limit=50000):
    """
    Fetch a limited number of records from an API endpoint using pagination.
    The function will stop once it has fetched the specified number of records.
    """
    all_data = []
    offset = 0

    while len(all_data) < limit:
        response = requests.get(endpoint_url, params={"limit": limit, "offset": offset})
        if response.status_code != 200:
            print(f"Failed to fetch data from {endpoint_url}: {response.status_code}")
            break

        data = response.json()
        if not data:  # Stop if no more data
            break

        all_data.extend(data)
        offset += len(data)  # Move to the next batch
        print(f"Fetched {len(data)} records, total so far: {len(all_data)}")

        if len(all_data) >= limit:
            break

    return all_data[:limit]


users_url = 'http://127.0.0.1:3000/users'
projects_url = 'http://127.0.0.1:3000/researches'

print("Fetching users data...")
users_data = fetch_data_from_endpoint_paginated(users_url, limit=50000)
print("Sample users data structure:", users_data[:2])

print("Fetching research projects data...")
projects_data = fetch_data_from_endpoint_paginated(projects_url, limit=50000)
print("Sample projects data structure:", projects_data[:2])

print("Converting data to DataFrames...")
users_df = pd.DataFrame(users_data)
projects_df = pd.DataFrame(projects_data)

print("\nUsers DataFrame structure:")
print(users_df.info())
print(users_df.head())

print("\nProjects DataFrame structure:")
print(projects_df.info())
print(projects_df.head())

required_users_columns = ['id']
required_projects_columns = ['creator_id']

missing_users_columns = [col for col in required_users_columns if col not in users_df.columns]
missing_projects_columns = [col for col in required_projects_columns if col not in projects_df.columns]

if missing_users_columns:
    print(f"Missing columns in users data: {missing_users_columns}")
if missing_projects_columns:
    print(f"Missing columns in projects data: {missing_projects_columns}")

if not missing_users_columns and not missing_projects_columns:
    print("\nAll required columns are present. Proceeding with merging...")
else:
    raise ValueError("Required columns are missing. Check the above output for details.")

print("\nMerging users and projects data...")
merged_df = pd.merge(users_df, projects_df, how='inner', left_on='id', right_on='creator_id')

print("\nMerged DataFrame structure:")
print(merged_df.info())
print(merged_df.head())

print("\nHandling missing values...")
merged_df.fillna(value={'name': 'Unknown', 'email': 'Unknown', 'title': 'No Title'}, inplace=True)

print("\nCleaned Data Description:")
print(merged_df.describe(include='all'))

print("\nSaving merged data to 'cleaned_merged_data.csv'...")
merged_df.to_csv("cleaned_merged_data.csv", index=False)
print("Saved successfully.")
