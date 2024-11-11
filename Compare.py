def get_rolling_hashes_from_db_row(row):
    """
    Convert the rolling hashes string from the database back into a list.
    The 'row' is expected to be a tuple where rolling hashes are in the third position (index 2).
    """
    rolling_hashes_str = row[3]  # Rolling hashes are stored as a comma-separated string in the DB.
    return rolling_hashes_str.split(',')

def compare_hashes(hashes1, hashes2):
    """Compare hashes from two lists and find similarities along with percentage similarity."""
    similarities = []
    
    # Use a dictionary for fast lookup
    hash_dict = {hash_value: index for index, hash_value in enumerate(hashes2)}
    
    for index1, hash1 in enumerate(hashes1):
        if hash1 in hash_dict:
            index2 = hash_dict[hash1]
            similarities.append((index1, index2, hash1))
    
    # Calculate similarity percentage
    if hashes1 and hashes2:
        total_hashes1 = len(hashes1)
        total_hashes2 = len(hashes2)
        matching_count = len(similarities)

        similarity_percentage = (matching_count / total_hashes1) * 100 if total_hashes1 > 0 else 0
    else:
        similarity_percentage = 0

    return {
        "similarities": similarities,
        "matching_count": matching_count,
        "total_hashes1": total_hashes1,
        "total_hashes2": total_hashes2,
        "similarity_percentage": similarity_percentage,
    }

def compare_against(new_file_hashes, db_rows):
    """Compare the hashes of a new file against all database rows."""
    comparison_results = []

    for row in db_rows:
        # Extract rolling hashes from database row
        rolling_hashes_from_db = get_rolling_hashes_from_db_row(row)
        
        # Compare hashes
        result = compare_hashes(new_file_hashes, rolling_hashes_from_db)
        
        # Append the results to the list
        comparison_results.append({
            "file_name": row[2],
            "similarities": result["similarities"],
            "matching_count": result["matching_count"],
            "total_hashes1": result["total_hashes1"],
            "total_hashes2": result["total_hashes2"],
            "similarity_percentage": result["similarity_percentage"],
        })

    return comparison_results
