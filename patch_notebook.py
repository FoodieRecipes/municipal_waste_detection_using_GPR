import json

with open("MSW_GPR_Forecasting_Uyo.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

new_cell_1_source = [
    "# Cell 1: Environment Diagnostic & Library Imports\n",
    "import sys\n",
    "import os\n",
    "\n",
    "# Ensure Python 3.14 packages are available\n",
    "py314_site = r'C:\\Users\\USER\\AppData\\Local\\Python\\pythoncore-3.14-64\\Lib\\site-packages'\n",
    "if os.path.exists(py314_site) and py314_site not in sys.path:\n",
    "    sys.path.insert(0, py314_site)\n",
    "\n",
    "print(f\"Active Python Executable: {sys.executable}\")\n",
    "print(f\"Active Python Version:    {sys.version.split()[0]}\")\n",
    "\n",
    "if '3.11' in sys.version:\n",
    "    print(\"\\n[!] WARNING: Your notebook is currently using Python 3.11 instead of Python 3.14!\")\n",
    "    print(\"[!] Please switch the notebook kernel to Python 3.14.2 in the top-right corner of VS Code:\")\n",
    "    print(\"[!] Click Kernel in Top-Right -> 'Python Environments...' -> 'Python 3.14.2'\")\n",
    "\n",
    "import joblib\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.dates as mdates\n",
    "import seaborn as sns\n",
    "from IPython.display import display\n",
    "\n",
    "from sklearn.gaussian_process import GaussianProcessRegressor\n",
    "from sklearn.gaussian_process.kernels import (\n",
    "    RBF, Matern, RationalQuadratic, DotProduct, ConstantKernel as C, WhiteKernel\n",
    ")\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.metrics import (\n",
    "    mean_squared_error, mean_absolute_error, r2_score, confusion_matrix, classification_report\n",
    ")\n",
    "\n",
    "sns.set_theme(style=\"whitegrid\")\n",
    "plt.rcParams[\"figure.figsize\"] = (12, 5)\n",
    "plt.rcParams[\"font.size\"] = 10\n",
    "\n",
    "print(\"\\n[OK] All required libraries imported successfully.\")\n"
]

for cell in nb["cells"]:
    if cell["cell_type"] == "code":
        cell["source"] = new_cell_1_source
        break

# Update notebook metadata to force Python 3.14.2
nb["metadata"] = {
    "kernelspec": {
        "display_name": "Python 3.14.2 64-bit",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "name": "python",
        "version": "3.14.2"
    }
}

with open("MSW_GPR_Forecasting_Uyo.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=2)

print("[OK] Patched MSW_GPR_Forecasting_Uyo.ipynb successfully!")

