
from resume_templates import (
    get_country_rules,
    get_supported_countries
)

# Show all supported countries
print("Supported countries:")
print(get_supported_countries())

# Get formatting rules for the USA
rules = get_country_rules("USA")

print("\nUSA resume rules:")
print(rules)

# Test an unsupported country
print("\nDefault rules:")
print(get_country_rules("Japan"))
