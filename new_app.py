import streamlit as st
import joblib
import numpy as np

# Load the pre-trained model
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

        # Check for missing values in critical fields
        if company == -1 or typename == -1 or ram == -1 or memory == -1 or gpu == -1 or opsys == -1 or resolution == -1:
            st.error("Please fill all the fields correctly.")
            return None
        
        # Combine all features into a list and ensure all values are numeric
        features = [
            company, typename, inches, ram, memory, gpu, opsys, weight, resolution, clockspeed, cpubrand, cputype
        ]
        
        # Convert the features to a numpy array
        features = np.array(features).reshape(1, -1)

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
            "🖥️ Use Toshiba PC Health Monitor to keep your laptop in good health.",
            "🔒 Regularly back up data using Toshiba's backup software.",
            "❄️ Keep the laptop cool using a cooling pad or by elevating the rear."
        ]
    }
    return tips.get(company, ["No tips available for this brand."])

# Streamlit UI elements
st.set_page_config(page_title="Laptop Price Prediction", page_icon="💻")

st.image("ai.webp", width=500)
# Add custom styling using HTML and CSS
st.markdown(""" 
    <style>
        body {
            background: linear-gradient(to right, #00c6ff, #0072ff);
            color: #fff;
            font-family: Arial, sans-serif;
        }
        .title {
            text-align: center;
            margin-top: 50px;
            font-size: 40px;
            font-weight: bold;
        }
        .image-container {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }
        .image-container img {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .form-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 50px;
            flex-wrap: wrap;
        }
        .form-container .block {
            background-color: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            width: 300px;
        }
        .btn-predict {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 18px;
            cursor: pointer;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: 0.3s;
        }
        .btn-predict:hover {
            background-color: #45a049;
        }
        .output {
            text-align: center;
            font-size: 28px;
            color: #FFD700;
        }
        .tips {
            margin-top: 30px;
            color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

# Header and Image Section
st.markdown('<div class="title">Laptop Price Prediction & Care Tips 💻</div>', unsafe_allow_html=True)



# Input Form Section
st.markdown('<div class="form-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    company = st.selectbox('🏢 Company', ['Apple', 'HP', 'Acer', 'Asus', 'Dell', 'Lenovo', 'Chuwi', 'MSI', 'Microsoft', 'Toshiba'])
    typename = st.selectbox('💼 Type', ['Ultrabook', 'Notebook', 'Gaming', '2 in 1 Convertible', 'Workstation', 'Netbook'])
    ram = st.selectbox('💾 RAM', ['8GB', '4GB', '16GB', '6GB', '12GB', '2GB', '32GB', '64GB', '24GB', '1GB'])
    memory = st.selectbox('💾 Storage', ['128GB SSD', '128GB Flash Storage', '256GB SSD', '512GB SSD', '500GB HDD', '256GB Flash Storage', '1TB HDD', '128GB SSD + 1TB HDD', '256GB Flash Storage'])
with col2:
    gpu = st.selectbox('🖥️ GPU', ['Intel Iris Plus Graphics 640', 'Intel HD Graphics 6000', 'Intel HD Graphics 620', 'AMD Radeon Pro 455'])
    opsys = st.selectbox('🖥️ Operating System', ['macOS', 'No OS', 'Windows 10', 'Mac OS X', 'Linux', 'Windows 10 S', 'Chrome OS', 'Windows 7', 'Android'])
    inches = st.number_input('📏 Screen Size (Inches)', min_value=10.0, max_value=17.0, step=0.1)
    weight = st.number_input('⚖️ Weight (kg)', min_value=0.5, max_value=5.0, step=0.1)
with col3:
    resolution = st.selectbox('🖥️ Screen Resolution', ['1366x768', '1920x1080', '3840x2160', '3200x1800', '2560x1600', '1920x1200', '1600x900', '2560x1440'])
    clockspeed = st.number_input('🖥️ Clock Speed (GHz)', min_value=1.0, max_value=5.0, step=0.1)
    cpubrand = st.selectbox('🔧 CPU Brand', ['Intel', 'AMD', 'Samsung'])
    cputype = st.selectbox('🔧 CPU Type', ['i3', 'i5', 'i7'])

# Prediction Button
st.markdown("</div>", unsafe_allow_html=True)
if st.button('🔍 Predict Price', key="predict_button", help="Click to predict laptop price", use_container_width=True):
    input_data = {
        'Company': company,
        'TypeName': typename,
        'Inches': inches,
        'Ram': ram,
        'Memory': memory,
        'Gpu': gpu,
        'OpSys': opsys,
        'Weight': weight,
        'ResolutionCategory': resolution,
        'Clock_Speed': clockspeed,
        'CPU_Brand': cpubrand,
        'CPU_Type': cputype
    }

    price = predict_price(input_data)

    if price:
        st.markdown(f'<div class="output">Predicted Price: ₹ {price[0]:,.2f}</div>', unsafe_allow_html=True)

    # Display care tips
    st.markdown('<div class="tips"><h3>Laptop Care Tips 📑</h3>', unsafe_allow_html=True)
    tips = laptop_tips(company)
    for tip in tips:
        st.markdown(f"<p>{tip}</p>", unsafe_allow_html=True)
