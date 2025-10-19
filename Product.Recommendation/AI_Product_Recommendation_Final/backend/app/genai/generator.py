"""Template-based Product Description Generator
This simple generator avoids pulling text from external sources.
It creates short, varied descriptions using product metadata.
"""
import random

def generate_description(title, brand, material, color, category):
    templates = [
        "The {title} from {brand} blends {material} craftsmanship with a {color} finish—perfect for {category}.",
        "Designed for comfort and style, {title} by {brand} features {material} material in {color}, suitable for {category} settings.",
        "Upgrade your space with the {title} ({brand}). A {color} {material} piece crafted for {category}.",
        "{brand} presents the {title}: {material} construction, {color} tone, tailored for {category}."
    ]
    t = random.choice(templates)
    return t.format(title=title, brand=brand or 'a trusted brand', material=material or 'quality', color=color or 'neutral', category=category or 'home')

if __name__ == '__main__':
    print(generate_description('Sample Chair','Acme','wood','brown','Living Room'))
