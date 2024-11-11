import hashlib
import mmap
import logging
from concurrent.futures import ThreadPoolExecutor

class FileHasher:
    def __init__(self, file_path: str, hash_function: str = "sha256"):
        self.file_path = file_path
        self.hash_function = hash_function
        self.valid_hashes = {"sha256": hashlib.sha256, "md5": hashlib.md5}

        if hash_function not in self.valid_hashes:
            raise ValueError(f"Unsupported hash function: {hash_function}")

    def compute_hash(self, data: bytes) -> str:
        """Compute a cryptographic hash for the given data (chunk/block)."""
        hash_func = self.valid_hashes[self.hash_function]()
        hash_func.update(data)
        return hash_func.hexdigest()

    def compute_full_file_hash(self) -> str:
        """Compute the full cryptographic hash for the entire file."""
        try:
            # Use the hash function incrementally over the file chunks
            hash_func = self.valid_hashes[self.hash_function]()
            with open(self.file_path, 'rb') as f:
                while chunk := f.read(8192):  # Read in 8 KB chunks
                    hash_func.update(chunk)  # Incrementally update the hash function
            return hash_func.hexdigest()  # Return the final hash (like a DNA fingerprint of the entire file)
        except Exception as e:
            logging.error(f"Error computing full hash for {self.file_path}: {e}")
            return None

    def calculate_rolling_hashes(self, block_size: int = 1024, parallel: bool = False) -> list:
        """Calculate 'DNA-like' rolling hashes for a file using the specified block size."""
        rolling_hashes = []
        try:
            with open(self.file_path, 'rb') as f:
                mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

                # Parallel or sequential computation of rolling hashes
                if parallel:
                    with ThreadPoolExecutor() as executor:
                        futures = {
                            executor.submit(self.compute_hash, mmapped_file[i:i + block_size]): i
                            for i in range(0, len(mmapped_file), block_size)
                        }
                        for future in futures:
                            try:
                                rolling_hashes.append(future.result())
                            except Exception as e:
                                logging.error(f"Error in parallel hash computation: {e}")
                else:
                    for i in range(0, len(mmapped_file), block_size):
                        data = mmapped_file[i:i + block_size]
                        rolling_hashes.append(self.compute_hash(data))

                mmapped_file.close()

        except Exception as e:
            logging.error(f"Error calculating rolling hashes for {self.file_path}: {e}")

        return rolling_hashes if rolling_hashes else None

    def save_hashes_to_file(self, rolling_hashes: list, output_path: str = "rolling_hashes.txt") -> None:
        """Save the DNA-like rolling hashes to a file."""
        try:
            with open(output_path, 'w') as out:
                for h in rolling_hashes:
                    out.write(f"{h}\n")
            logging.info(f"Rolling hashes saved to {output_path}")
        except Exception as e:
            logging.error(f"Error saving rolling hashes to {output_path}: {e}")
