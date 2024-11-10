import streamlit as st
import joblib
import numpy as np

# Load the pre-trained model without success message
try:
    model = joblib.load("laptop.pkl")  # Adjust path if necessary
except Exception as e:
    st.error(f"Error loading model: {e}")

# Feature mappings for the categorical variables
company_mapping = {
    'Apple': 1, 'HP': 7, 'Acer': 0, 'Asus': 2, 'Dell': 4, 'Lenovo': 10, 'Chuwi': 3,
    'MSI': 11, 'Microsoft': 13, 'Toshiba': 16, 'Huawei': 8, 'Xiaomi': 18, 'Vero': 17,
    'Razer': 14, 'Mediacom': 12, 'Samsung': 15, 'Google': 6, 'Fujitsu': 5, 'LG': 9
}

type_mapping = {
    'Ultrabook': 4, 'Notebook': 3, 'Gaming': 1, '2 in 1 Convertible': 0, 
    'Workstation': 5, 'Netbook': 2
}

ram_mapping = {
    '8GB': 9, '4GB': 1, '16GB': 6, '6GB': 4, '12GB': 0, '2GB': 7, '32GB': 8, 
    '64GB': 5, '24GB': 3, '1GB': 2
}

memory_mapping = {
    '128GB SSD': 1, '128GB Flash Storage': 7, '256GB SSD': 12, '512GB SSD': 10, 
    '500GB HDD': 4, '256GB Flash Storage': 13, '1TB HDD': 9, '128GB SSD + 1TB HDD': 8,
    '256GB Flash Storage': 0, '64GB Flash Storage': 2, '32GB Flash Storage': 3,
    '256GB SSD + 256GB SSD': 5, '256GB SSD + 1TB HDD': 6, '256GB SSD + 2TB HDD': 11,
    '1TB SSD': 18, '2TB HDD': 28, '512GB SSD + 1TB HDD': 17
}

cpu_brand_mapping = {
    'Intel': 0, 'AMD': 1, 'Samsung': 2
}

cpu_type_mapping = {
    'i3': 2, 'i5': 1, 'i7': 0
}

gpu_mapping = {
    'Intel Iris Plus Graphics 640': 0, 'Intel HD Graphics 6000': 1, 'Intel HD Graphics 620': 2, 
    'AMD Radeon Pro 455': 3, 'Intel Iris Plus Graphics 650': 4, 'AMD Radeon R5': 5, 
    'Intel Iris Pro Graphics': 6, 'Nvidia GeForce MX150': 7, 'Intel UHD Graphics 620': 8, 
    'Intel HD Graphics 520': 9, 'AMD Radeon Pro 555': 10, 'AMD Radeon R5 M430': 11, 
    'Intel HD Graphics 615': 12, 'AMD Radeon Pro 560': 13, 'Nvidia GeForce 940MX': 14, 
    'Nvidia GeForce GTX 1050': 15, 'AMD Radeon R2': 16, 'AMD Radeon 530': 17, 'Nvidia GeForce 930MX': 18,
    'Intel HD Graphics': 19, 'Intel HD Graphics 500': 20, 'Nvidia GeForce 930MX ': 21, 
    'Nvidia GeForce GTX 1060': 22
}

resolution_mapping = {
    '1366x768': 0, '1920x1080': 1, '3840x2160': 2, '3200x1800': 3, '2560x1600': 4, 
    '1920x1200': 5, '1600x900': 6, '2560x1440': 7
}

opsys_mapping = {
    'macOS': 8, 'No OS': 4, 'Windows 10': 5, 'Mac OS X': 3, 'Linux': 6,
    'Windows 10 S': 1, 'Chrome OS': 7, 'Windows 7': 0, 'Android': 2
}

# Function to predict price based on user input
def predict_price(input_data):
    try:
        # Extract individual feature values and apply mappings
        company = company_mapping.get(input_data['Company'], -1)
        typename = type_mapping.get(input_data['TypeName'], -1)
        inches = input_data['Inches']
        ram = ram_mapping.get(input_data['Ram'], -1)
        memory = memory_mapping.get(input_data['Memory'], -1)
        gpu = gpu_mapping.get(input_data['Gpu'], -1)
        opsys = opsys_mapping.get(input_data['OpSys'], -1)
        weight = input_data['Weight']
        resolution = resolution_mapping.get(input_data['ResolutionCategory'], -1)
        clockspeed = input_data['Clock_Speed']
        cpubrand = cpu_brand_mapping.get(input_data['CPU_Brand'], -1)
        cputype = cpu_type_mapping.get(input_data['CPU_Type'], -1)

        # Check for missing values in critical fields (map to -1 if invalid)
        if company == -1 or typename == -1 or ram == -1 or memory == -1 or gpu == -1 or opsys == -1 or resolution == -1:
            st.error("Please fill all the fields correctly.")
            return None
        
        # Combine all features into a list and ensure all values are numeric
        features = [
            company, typename, inches, ram, memory, gpu, opsys, weight, resolution, clockspeed, cpubrand, cputype
        ]
        
        # Convert the features to a numpy array
        features = np.array(features).reshape(1, -1)

        # Check for any missing or invalid values in the features
        if np.any(features == -1):
            st.error("Some input features are invalid. Please check your input values.")
            return None
        
        # Ensure there are no unexpected unicode or string characters
        features = features.astype(np.float32)

        # Make the prediction
        prediction = model.predict(features)
        return prediction
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None

# Laptop care and usage tips based on the selected brand
def laptop_tips(company):
    tips = {
        "Apple": [
            "📱 Always use a soft microfiber cloth to clean your MacBook screen and keyboard.",
            "🔒 Regularly back up your data with Time Machine or iCloud.",
            "🌡️ Avoid exposing your MacBook to extreme temperatures to preserve battery life."
        ],
        "HP": [
            "🌀 Keep the laptop vents clear to prevent overheating.",
            "🔄 Regularly update your HP software to ensure better performance.",
            "❄️ Use an HP recommended laptop cooler for extended use to maintain optimal performance."
        ],
        "Acer": [
            "💡 Use Acer’s built-in care tools for battery health management.",
            "🧹 Clean the keyboard and screen with a soft cloth regularly.",
            "⚖️ Avoid putting heavy pressure on your Acer laptop to prevent screen damage."
        ],
        "Asus": [
            "🔧 Ensure your Asus laptop runs its regular diagnostics for better performance.",
            "🧹 Regularly clean the fans to avoid dust buildup and overheating.",
            "🔋 Adjust screen brightness to save battery when not plugged in."
        ],
        "Dell": [
            "🔋 Use Dell's Power Manager to improve battery life.",
            "🌬️ Keep your Dell laptop in a well-ventilated area to prevent heating.",
            "🔄 Make use of Dell SupportAssist for updates and maintenance."
        ],
        "Lenovo": [
            "🔧 Use Lenovo Vantage for driver and software updates.",
            "🔋 Periodically check your Lenovo laptop's battery health.",
            "🧹 Keep your laptop's cooling vents clean to avoid overheating."
        ],
        "Chuwi": [
            "🧹 Clean the device gently with a soft cloth.",
            "🛠️ Update Chuwi drivers for optimal performance.",
            "🌬️ Ensure proper ventilation to prevent overheating during long usage."
        ],
        "MSI": [
            "⚙️ Use MSI Dragon Center to adjust performance settings for gaming.",
            "🧹 Regularly clean your laptop’s fans to prevent overheating.",
            "❄️ Use a cooling pad for better thermal performance when gaming."
        ],
        "Microsoft": [
            "🔄 Use Windows Update to keep your Surface running smoothly.",
            "🔋 Always charge your Microsoft laptop when the battery goes below 20%.",
            "🧼 Clean the Surface screen using a microfiber cloth to prevent scratches."
        ],
        "Toshiba": [
            "🖥️ Ensure you have updated your Toshiba laptop drivers.",
            "💧 Do not expose the laptop to moisture or extreme temperatures.",
            "🔋 Use Toshiba's eco-mode to extend battery life."
        ]
    }
    
    return tips.get(company, [])

# Streamlit user interface
st.set_page_config(page_title="Laptop Price Prediction and Tips", page_icon="💻")

# Background color and font styles
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        .title {
            color: #962205;
            font-size: 36px;
            font-weight: bold;
        }
        .company-name {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 18px;
            color: gray;
        }
        .sidebar .sidebar-content {
            background-color: #f9f9f9;
        }
        .prediction {
            font-size: 24px;
            color: #FF5733;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .tips {
            font-size: 18px;
            margin-top: 30px;
        }
        .highlight-price {
            color: #FF5733;
            font-size: 30px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Header with image and title
st.markdown('<div class="title">Laptop Price Prediction 💻</div>', unsafe_allow_html=True)
st.image('ai.webp', caption='Laptop Price Prediction App', width=450)

# Sidebar inputs with emojis
company = st.sidebar.selectbox('🏢 Company', ['Apple', 'HP', 'Acer', 'Asus', 'Dell', 'Lenovo', 'Chuwi', 
                                               'MSI', 'Microsoft', 'Toshiba', 'Huawei', 'Xiaomi', 'Vero', 
                                               'Razer', 'Mediacom', 'Samsung', 'Google', 'Fujitsu', 'LG'])

typename = st.sidebar.selectbox('💼 Type', ['Ultrabook', 'Notebook', 'Gaming', '2 in 1 Convertible', 
                                           'Workstation', 'Netbook'])

inches = st.sidebar.number_input('📏 Screen Size (Inches)', min_value=10.0, max_value=17.0, step=0.1)

ram = st.sidebar.selectbox('💾 RAM', ['8GB', '4GB', '16GB', '6GB', '12GB', '2GB', '32GB', '64GB', '24GB', '1GB'])

memory = st.sidebar.selectbox('💾 Storage', ['128GB SSD', '128GB Flash Storage', '256GB SSD', '512GB SSD', '500GB HDD', 
                                             '256GB Flash Storage', '1TB HDD', '128GB SSD + 1TB HDD', '256GB Flash Storage',
                                             '64GB Flash Storage', '32GB Flash Storage', '256GB SSD + 256GB SSD', 
                                             '256GB SSD + 1TB HDD', '256GB SSD + 2TB HDD', '1TB SSD', '2TB HDD', 
                                             '512GB SSD + 1TB HDD'])

gpu = st.sidebar.selectbox('🖥️ GPU', ['Intel Iris Plus Graphics 640', 'Intel HD Graphics 6000', 'Intel HD Graphics 620', 
                                       'AMD Radeon Pro 455', 'Intel Iris Plus Graphics 650', 'AMD Radeon R5', 
                                       'Intel Iris Pro Graphics', 'Nvidia GeForce MX150', 'Intel UHD Graphics 620', 
                                       'Intel HD Graphics 520', 'AMD Radeon Pro 555', 'AMD Radeon R5 M430', 
                                       'Intel HD Graphics 615', 'AMD Radeon Pro 560', 'Nvidia GeForce 940MX', 
                                       'Nvidia GeForce GTX 1050', 'AMD Radeon R2', 'AMD Radeon 530', 'Nvidia GeForce 930MX'])

opsys = st.sidebar.selectbox('🖥️ Operating System', ['macOS', 'No OS', 'Windows 10', 'Mac OS X', 'Linux', 'Windows 10 S', 
                                                     'Chrome OS', 'Windows 7', 'Android'])

weight = st.sidebar.number_input('⚖️ Weight (kg)', min_value=0.0, max_value=10.0, step=0.1)

resolution_category = st.sidebar.selectbox('🔲 Resolution', ['1366x768', '1920x1080', '3840x2160', 
                                                             '3200x1800', '2560x1600', '1920x1200', 
                                                             '1600x900', '2560x1440'])

clock_speed = st.sidebar.number_input('⏱️ Clock Speed (GHz)', min_value=0.0, max_value=5.0, step=0.1)

cpu_brand = st.sidebar.selectbox('💻 CPU Brand', ['Intel', 'AMD', 'Samsung'])

cpu_type = st.sidebar.selectbox('🖱️ CPU Type', ['i3', 'i5', 'i7'])

# Prepare input data for prediction
input_data = {
    'Company': company, 'TypeName': typename, 'Inches': inches, 'Ram': ram, 'Memory': memory, 
    'Gpu': gpu, 'OpSys': opsys, 'Weight': weight, 'ResolutionCategory': resolution_category,
    'Clock_Speed': clock_speed, 'CPU_Brand': cpu_brand, 'CPU_Type': cpu_type
}

# When button is clicked, predict and display the result
if st.sidebar.button('🔮 Predict Price'):
    predicted_price = predict_price(input_data)
    if predicted_price is not None:
        st.markdown(f"<div class='highlight-price'>The predicted price is: ₹{predicted_price[0]:,.2f}</div>", unsafe_allow_html=True)

    # Display laptop care tips based on selected company
    tips = laptop_tips(company)
    st.markdown('<div class="tips">### 🛠️ Usage and Care Tips for selected laptop_company :</div>', unsafe_allow_html=True)
    for tip in tips:
        st.write(tip)

# Custom CSS for positioning the company name in the top right corner
st.markdown("""
    <style>
        .company-name {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 18px;
            color: gray;
        }
    </style>
    <div class="company-name">SmartTech Co.</div>
""", unsafe_allow_html=True)
