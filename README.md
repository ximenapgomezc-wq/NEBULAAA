# Nebulaaa - Weather Prediction Web App

## Description
Will it rain on my parade? NASA Space apps challenge. Our project predicts the probability of a certain weathers in the long run. This is to say a person could search for the weather in any place in the world months in advanced and get an accurate prediction based on last year's weather"

---

## Prerequisites

Before running the application, make sure your system meets the following requirements:

- **Python version:** 3.12.x is recommended.  
  > ⚠️ If you are using Python 3.13.x (especially on Windows 11), some packages like `pandas==2.2.2` may fail to install. To avoid issues, it is best to use Python 3.12.x when setting up the virtual environment.

- **Virtual environment:** It is highly recommended to create a virtual environment to isolate dependencies.  

- **Required packages:** All dependencies are listed in `requirements.txt` and can be installed using `pip install -r requirements.txt` after activating the virtual environment.

- **GitHub:** Git must be installed to clone or download the project repository.  
  > ⚠️ You do **not** need a GitHub account to run the project locally; an account is only required if you want to push changes to the repository.

---

## Download the project from GitHub

Clone the repository using the following command:

```bash
git clone https://github.com/ximenapgomezc-wq/NEBULAAA.git
cd NEBULAAA
```

---

## Project Structure

```
Nebulaaa/
├── app.py                     # Backend using Flask
├── data/
│   └── weather_summary_intento18_2_2024_WORLD_CAPITALS_195_3days.csv  # Historical weather data
├── static/
│   └── script.js               # Frontend logic (JS)
├── templates/
│   └── index.html              # Web interface
├── README.md
└── requirements.txt            # Python dependencies
```

> Tip: The directory structure uses proper tree-style formatting. GitHub should display it correctly.

---

## How to Run Locally

### 1️⃣ Create a virtual environment

This ensures dependencies are installed in isolation.

```bash
python -m venv venv
```

### 2️⃣ Activate the virtual environment

- **Mac/Linux:**

```bash
source venv/bin/activate
```

- **Windows:**

```bash
venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the application

```bash
python app.py
```

The application will run at:

```
http://127.0.0.1:5000
```

Open it in your browser to access the dashboard.

---

## Usage

1. Select the **city** and the **date**.  
2. Click **Predict**.  
3. Check the results:  
   - **Cards** with metrics for temperature, precipitation, wind, humidity, and cloud top temperature.  
   - **Charts** showing trends for the last 3 days in the dataset.  
   - **Map** displaying the location of the selected city.  

> Temperatures are displayed in **Celsius (°C)**, and other metrics follow the dataset units.

---

## Notes

- The `scripts/` folder contains auxiliary scripts used to generate or update the CSV files.  
- Keep `data/weather_summary_intento18_2_2024_WORLD_CAPITALS_195_3days.csv` in place; the app relies on it.  
- Use the provided `requirements.txt` to replicate the environment.  

---

## Optional: Polished GitHub Showcase

You can add badges (Python version, license, etc.) and screenshots for a more professional README.
