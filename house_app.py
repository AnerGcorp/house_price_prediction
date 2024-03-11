import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load(open("xgb_model.joblib", "rb"))

# Load the list of features
columns = joblib.load("features_list.joblib")

# Function to predict house price
def predict_price(features):
    sample_df = pd.DataFrame(features, columns=columns)
    pred_price = round(model.predict(sample_df)[0])
    return pred_price

# Page title and image
st.title("House Price Prediction")
image = open("house.jpeg", "rb").read()
st.image(image, caption='House', use_column_width=True)

# Inputs
st.header('Enter House Details')
overall_qual = st.number_input('Overall Quality (1-10)', min_value=1)
garage_cars = st.number_input('Garage Cars', min_value=0)
central_air = st.radio('Central Air Conditioning', ['Yes', 'No'])
living_area = st.slider('Living Area (sqft)', min_value=334, max_value=5642)
garage_type = st.selectbox('Garage Type', ['More than one type of garage', 'Attached to home', 'Basement Garage', 'Built-In', 'Car Port', 'Detached from home', 'No Garage'])
basement_sf = st.slider('Basement Area (sqft)', min_value=42.0, max_value=2052.0)

# Create three columns for input fields
col1, col2, col3 = st.columns(3)

# Garage Quality select box
with col1:
    garage_qual = st.selectbox('Garage Quality', ['Excellent', 'Good', 'Average', 'Fair', 'Poor', 'No Garage'])

# Kitchen Quality select box
with col2:
    kitchen_qual = st.selectbox('Kitchen Quality', ['Excellent', 'Good', 'Average', 'Fair', 'Poor'])

# Fireplace Quality select box
with col3:
    fireplace_qual = st.selectbox('Fireplace Quality', ['Excellent', 'Good', 'Average', 'Fair', 'Poor', 'No Fireplace'])

land_contour = st.number_input('Land Contour', min_value=1, max_value=4)

# User input dictionary
sample_one = pd.DataFrame({
    'OverallQual': [overall_qual],
    'GarageCars': [garage_cars],
    'CentralAir_Y': [1 if central_air == 'Yes' else 0],  # Convert 'Yes'/'No' to 1/0
    'GrLivArea': [living_area],
    'GarageType': [garage_type],
    'TotalBsmtSF': [basement_sf],
    'GarageQual': [garage_qual],
    'KitchenQual': [kitchen_qual],
    'FireplaceQu': [fireplace_qual],
    'LandContour': [land_contour]
})


# Apply mappings for categorical variables
kitchen_qual_mapping = {'Excellent': 0, 'Good': 2, 'Average': 5, 'Fair': 1, 'Poor': 4}
sample_one['KitchenQual'] = sample_one['KitchenQual'].map(kitchen_qual_mapping)

fireplace_qu_mapping = {'Excellent': 0, 'Good': 2, 'Average': 5, 'Fair': 1, 'Poor': 4, 'No Fireplace': 3}
sample_one['FireplaceQu'] = sample_one['FireplaceQu'].map(fireplace_qu_mapping)

garage_qu_mapping = {'Excellent': 0, 'Good': 2, 'Average': 5, 'Fair': 1, 'Poor': 4, 'No Garage': 3}
sample_one['GarageQual'] = sample_one['GarageQual'].map(garage_qu_mapping)

garage_type_mapping = {'More than one type of garage': 0, 'Attached to home': 1, 'Basement Garage': 2, 
                       'Built-In': 3, 'Car Port': 4, 'Detached from home': 5, 'No Garage': 6}
sample_one['GarageType'] = sample_one['GarageType'].map(garage_type_mapping)

# Preprocess user input
#preprocessed_input_flat = preprocess_input(sample_one)
if st.button('Predict Price'):
    predicted_price = predict_price(sample_one)
    st.write(f"Predicted House Price: ${predicted_price}")
