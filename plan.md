## What your app will do (plain English)
Load your CSV of pandals (name + latitude + longitude).
Ask the user for their current location (lat, lon).
Compute distance from the user to every pandal.
Sort by distance and show the nearest first.
(Nice-to-have) Show them on a map and give a Google Maps link for directions.

Think of it like: input (your location) → math (distance) → sorted list → map + links.


# Streamlit skeleton (folders + files)
your-project/
  ├─ app.py
  ├─ pandal_loc.csv
  └─ requirements.txt

# Mini checklist (you can copy this)
CSV has name, latitude, longitude columns with numeric values.
Haversine function tested with a simple example.
Manual lat/lon input works. 
Distances computed + sorted; top 10 displayed.
Directions links open correctly.
Map shows points in the right city.
Optional: auto-detect user location.
Deployed to Streamlit Cloud.