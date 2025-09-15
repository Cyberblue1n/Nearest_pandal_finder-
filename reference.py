import streamlit as st
import pandas as pd
import math
import streamlit.components.v1 as components

# Haversine distance function
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1-a))

# Load pandal data
try:
    df = pd.read_csv("pandal_loc2.csv")
    st.success(f"✅ Loaded {len(df)} pandals from database")
except FileNotFoundError:
    st.error("❌ Could not find pandal_loc.csv file. Please make sure it exists in the parent directory.")
    st.stop()

st.title("🏮 Durga Puja Nearest Pandal Finder")
st.markdown("Find the closest Durga Puja pandals from your location")

# Add some information about how to get coordinates
st.info("💡 **How to get your coordinates:**\n"
        "1. **Click 'Detect My Location' button below** (automatic)\n"
        "2. If option 1 doesn't work, Open Google Maps → Long press your location → Copy from search bar\n")

# Simple location detection
if st.button("📍 Detect My Location", type="primary", help="Get your current coordinates automatically"):
    # Simple HTML/JavaScript for location detection
    location_html = """
    <div id="location-result" style="padding: 5px; border-radius: 8px; background: #f0f7ff; font-family: sans-serif;">
        🔄 Getting your location...
    </div>
    
    <script>
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude.toFixed(6);
                const lon = position.coords.longitude.toFixed(6);
                document.getElementById('location-result').innerHTML = 
                    `✅ <strong>Location detected!</strong><br>
                     📍 Latitude: <strong>${lat}</strong><br>
                     📍 Longitude: <strong>${lon}</strong><br>
                     <small style="color: #666;">Copy these values to the input fields below</small>`;
                document.getElementById('location-result').style.background = '#e8f5e8';
            },
            function(error) {
                let message = '❌ ';
                if (error.code === 1) message += 'Location access denied. Please allow location access.';
                else if (error.code === 2) message += 'Location unavailable. Check your connection.';
                else if (error.code === 3) message += 'Location request timed out. Try again.';
                else message += 'Failed to get location.';
                
                document.getElementById('location-result').innerHTML = message;
                document.getElementById('location-result').style.background = '#ffebee';
            },
            {enableHighAccuracy: true, timeout: 10000}
        );
    } else {
        document.getElementById('location-result').innerHTML = '❌ Geolocation not supported by this browser.';
        document.getElementById('location-result').style.background = '#ffebee';
    }
    </script>
    """
    components.html(location_html, height=100)

# User location input
col1, col2 = st.columns(2)
with col1:
    lat = st.text_input("📍 Enter your Latitude", value=22.5744, help="Example: 22.5744")
    lat = float(lat) if lat else 0.0
with col2:
    lon = st.text_input("📍 Enter your Longitude", value=88.3629, help="Example: 88.3629")
    lon = float(lon) if lon else 0.0

# Add validation for coordinates
if lat == 0.0 and lon == 0.0:
    st.warning("⚠️ Please enter your actual coordinates above")
elif not (22.0 <= lat <= 23.0 and 88.0 <= lon <= 89.0):
    st.warning("⚠️ Coordinates seem to be outside Kolkata area. Please double-check your location.")

if st.button("🔍 Find Nearest Pandals", type="primary"):
    if lat == 0.0 or lon == 0.0:
        st.error("❌ Please enter your coordinates first!")
    else:
        with st.spinner("🔍 Calculating distances to all pandals..."):
            df["Distance_km"] = df.apply(lambda row: haversine(lat, lon, row["latitude"], row["longitude"]), axis=1)
            
            # Apply road factor (tune this number, e.g., 1.3 for Kolkata)
            ROAD_FACTOR = 1.3
            df["Estimated_Road_km"] = df["Distance_km"] * ROAD_FACTOR
            nearest = df.sort_values("Estimated_Road_km").head(10)  # Show top 10 instead of 5
        
        st.subheader("🏮 Nearest Pandals to Your Location:")
        
        for i, (_, row) in enumerate(nearest.iterrows(), 1):
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    st.markdown(f"**#{i}**")
                
                with col2:
                    st.markdown(f"**{row['name']}**")
                    st.markdown(f"📍 Area: {row['area']}")
                    st.markdown(f"🚶‍♂️ Estimated Distance: **{row['Estimated_Road_km']:.2f} km**")
                
                with col3:
                    st.markdown(f"[🗺️ Go to Map](https://www.google.com/maps/search/?api=1&query={row['latitude']},{row['longitude']})")
                    st.markdown(f"[🧭 Directions](https://www.google.com/maps/dir/?api=1&destination={row['latitude']},{row['longitude']})")
                
                st.divider()
        
        # Show some statistics
        st.subheader("📊Estimated Statistics:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Closest Pandal(℮)", f"{nearest.iloc[0]['Estimated_Road_km']:.2f} km")
        
        with col2:
            st.metric("Farthest (in top 10)(℮)", f"{nearest.iloc[-1]['Estimated_Road_km']:.2f} km")
        
        with col3:
            within_5km = len(nearest[nearest['Estimated_Road_km'] <= 5])
            st.metric("Within 5km", f"{within_5km} pandals")

