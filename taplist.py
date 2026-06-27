import xml.etree.ElementTree as ET
from datetime import datetime

INPUT_FILE = "beers.xml"
OUTPUT_FILE = "index.html"

def get_text(parent, tag):
    el = parent.find(tag)
    return el.text.strip() if el is not None and el.text else ""

# -------- LOAD XML --------
tree = ET.parse(INPUT_FILE)
root = tree.getroot()

beers = []

for recipe in root.findall(".//RECIPE"):

    # ✅ FILTER: Only beers marked "On Tap"
    assistant = get_text(recipe, "ASST_BREWER").lower()
    if assistant != "on tap":
        continue

    style = recipe.find("STYLE")

    # ✅ Get description ONLY (no fallback)
    description = get_text(recipe, "TASTE_NOTES")

    # ✅ Format brewed date nicely
    
    raw_date = get_text(recipe, "DATE")

    try:
        # Parse full BeerSmith format including time
        dt = datetime.strptime(raw_date, "%d %b %Y %H:%M:%S")

        # Format without time
        brewed_date = dt.strftime("%d %b %Y")
    except:
        brewed_date = raw_date

    beer = {
        "name": get_text(recipe, "NAME"),
        "style": get_text(style, "NAME") if style is not None else "",
        "abv": get_text(recipe, "ABV"),
        "ibu": get_text(recipe, "IBU"),
        "description": description,
        "brewed": brewed_date
    }

    beers.append(beer)

# -------- SORT (optional but nice) --------
beers.sort(key=lambda x: x["name"])

# -------- GENERATE HTML --------
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta charset="UTF-8">
<title>Beer Menu</title>
<style>
body {{
    max-width: 600px;
    margin: auto;
    padding: 25px;
    font-family: Arial, sans-serif;
    background-color: #1c1c1c;
    color: #f5f5f5;
}}

h1 {{
    text-align: center;
    font-size: 2em;
    margin-bottom: 10px;
}}

.updated {{
    text-align: center;
    font-size: 0.8em;
    color: #aaa;
    margin-bottom: 25px;
}}

.beer {{
    border-bottom: 1px solid #444;
    padding: 12px 0;
}}

.name {{
    font-size: 1.5em;
    font-weight: bold;
}}

.meta {{
    color: #ccc;
    font-size: 0.95em;
}}

.desc {{
    margin-top: 5px;
    font-style: italic;
    color: #ddd;
}}
</style>
</head>

<body>

<h1>🍺 Beer Menu</h1>
<p class="updated">Updated: {datetime.now().strftime("%d %b %Y %H:%M")}</p>
"""

for b in beers:
    html += f"""
    <div class="beer">
        <div class="name">{b['name']}</div>
        <div class="meta">
            {b['style']} | {b['abv']} ABV | {b['ibu']}
        </div>
        <div class="meta">
            Brewed: {b['brewed']}
        </div>
    """

    # ✅ Only show description if present
    if b["description"]:
        html += f"""
        <div class="desc">
            {b['description']}
        </div>
        """

    html += "</div>"

html += """
</body>
</html>
"""

# -------- SAVE FILE --------
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Menu created:", OUTPUT_FILE)