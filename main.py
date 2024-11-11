import os
import DatabaseManager
import RollingHash
import Compare

# Directory containing the files
# old_directory = r'old'

# # Create the database if it doesn't exist
# DatabaseManager.create_database()

# # Iterate over all files in the old directory
# for file_name in os.listdir(old_directory):
#     file_path = os.path.join(old_directory, file_name)

#     # Only process if it's a file (ignores subdirectories)
#     if os.path.isfile(file_path):
#         file_hasher = RollingHash.FileHasher(file_path)
#         full_hash = file_hasher.compute_full_file_hash()
        
#         if full_hash:
#             # Insert hash into the database
#             DatabaseManager.insert_hash(full_hash, file_name, file_hasher.calculate_rolling_hashes(block_size=500,parallel=True))
#             print(f"Processed and added file: {file_name}")
#         else:
#             print(f"Could not compute hash for file: {file_name}")

# Now, we will compare the new file's hashes against the database
# Get all hashes from the database
db_rows = DatabaseManager.get_all_hashes()

# Initialize FileHasher for the new file
new_file_path = r'old\file1.txt'  # Replace with your target file
file_hasher = RollingHash.FileHasher(new_file_path)

# Compute rolling hashes for the new file
new_file_hashes = file_hasher.calculate_rolling_hashes(block_size=500,parallel=True)

# Compare the new file hashes against the database
comparison_results = Compare.compare_against(new_file_hashes, db_rows)

# Print or process the comparison results
for result in comparison_results:
    print(f"\n Comparing against file: {result['file_name']}")
    print(f"Matching Count: {result['matching_count']} out of {result['total_hashes1']} hashes.")
    print(f"Similarity Percentage: {result['similarity_percentage']:.2f}% \n")
    print(f"Similar Hashes: {result['similarities']}\n")

