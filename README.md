# 🔥 AI-Powered Heatmap Generator

## ✨ Overview
**AI-Powered Heatmap Generator** is an intuitive **customtkinter-based** desktop application that allows users to create **correlation heatmaps** from **CSV, Excel, or MySQL databases**. It leverages **Google Gemini AI** to suggest heatmap names and provide analytical insights on data patterns.

With a sleek **dark-themed UI**, this tool is perfect for data analysts, researchers, and anyone looking to visualize and interpret their data with ease.

---

## 📈 Features
- 🔍 **Data Source Selection:** Load data from **CSV, Excel, or MySQL**.
- ⚙️ **AI-Powered Insights:** Gemini AI **suggests heatmap names** and provides **data analysis**.
- 🌌 **Customizable UI:** Built with **CustomTkinter**, offering a modern and dark-mode interface.
- 🎨 **Seaborn Heatmaps:** Generate beautifully formatted **correlation heatmaps**.
- 📂 **Save & Export:** Save heatmaps as **PNG or JPEG** for future use.

---

## 🛠️ Installation
### Prerequisites
Ensure you have **Python 3.8+** installed along with the required dependencies.

```bash
pip install customtkinter pandas seaborn matplotlib mysql-connector-python google-generativeai
```

### Clone the Repository
```bash
git clone https://github.com/Alpha-Cassius/AI-Powered-Heatmap-Generator.git
cd AI-Heatmap-Generator
```

---

## 💪 Usage
### Run the Application
```bash
python main.py
```

### Steps:
1. **Select Data Source:** Choose between **CSV, Excel, or MySQL**.
2. **Load Data:** Browse and select a file or enter MySQL credentials.
3. **Generate Heatmap:** Click the **Generate Heatmap** button.
4. **AI Insights:** Let **Gemini AI** suggest a heatmap name and analyze the data.
5. **Save Heatmap:** Export your visualization as **PNG or JPEG**.

---

## 🌟 Screenshots
### **Main Interface**
![App UI](https://via.placeholder.com/800x400?text=Main+Interface)

### **Generated Heatmap**
![Heatmap](https://via.placeholder.com/800x400?text=Sample+Heatmap)

---

## 💡 API Configuration
This project requires **Google Gemini AI API**. Set up your API key:

```python
os.environ['GOOGLE_API_KEY'] = "YOUR_API_KEY"
```
Replace `YOUR_API` with your **actual API key** from **Google Generative AI**.

---

## ⚡ Contributing
Feel free to **fork** this repository and submit a **pull request** with enhancements or bug fixes!

1. **Fork** the project
2. **Create a feature branch** (`git checkout -b feature-name`)
3. **Commit your changes** (`git commit -m "Add new feature"`)
4. **Push to your branch** (`git push origin feature-name`)
5. **Open a Pull Request**

---

## 👨‍💻 Author
**Vaibhav Pandey**  
GitHub: [@your-username](https://github.com/Alpha-Cassius)

---

## ⚖️ License
This project is licensed under the **MIT License**. Feel free to use, modify, and distribute!

---

## 📢 Acknowledgments
- **CustomTkinter** for the modern UI
- **Seaborn & Matplotlib** for beautiful visualizations
- **Google Gemini AI** for intelligent insights

---

Made with ❤️ by Vaibhav Pandey

