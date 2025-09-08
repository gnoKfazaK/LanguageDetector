import time

class TimeBasedCache:
    def __init__(self, ttl):
        """Initialize the cache with a specified time-to-live (TTL) in seconds."""
        self.ttl = ttl
        self.cache = {}

    def put(self, key, value):
        """Store the value in the cache with the current timestamp."""
        self.cache[key] = (value, time.time())

    def get(self, key):
        """Retrieve the value from the cache if it hasn't expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                # If expired, remove it from the cache
                del self.cache[key]
        return None  # Return None if key doesn't exist or has expired

    def delete(self, key):
        """Remove the specified key from the cache."""
        if key in self.cache:
            del self.cache[key]

    def exists(self, key):
        """Check if a key exists in the cache and hasn't expired."""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return True
            else:
                del self.cache[key]  # Remove expired entry
        return False

    def cleanup(self):
        """Remove all expired entries from the cache."""
        current_time = time.time()
        keys_to_delete = [key for key in self.cache if current_time - self.cache[key][1] >= self.ttl]
        for key in keys_to_delete:
            del self.cache[key]
