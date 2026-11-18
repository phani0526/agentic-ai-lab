class UserProfile:
    def __init__(self, first_name: str, last_name: str):
        # These are the actual stored data fields
        self.first_name = first_name
        self.last_name = last_name

    # This is a convenience property
    @property
    def full_name(self) -> str:
        # It computes the value on the fly when accessed
        return f"{self.first_name} {self.last_name}"


# 1. Create an instance of our class
user = UserProfile(first_name="Jane", last_name="Doe")

# 2. Accessing it like a regular attribute (notice NO parentheses `()`)
print(user.full_name)  # Output: Jane Doe

# 3. What happens if we convert the object to a dictionary?
# (simulating how SDKs dump their raw fields)
print(user.__dict__)  # Output: {'first_name': 'Jane', 'last_name': 'Doe'}
