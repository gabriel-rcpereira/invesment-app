# Investment Helper

This project provides Python scripts to help users analyze and visualize their investment data, including fixed income, stock market, and treasury investments. The scripts process data from Excel files, calculate key metrics, and generate visualizations such as bar charts and pie charts to provide insights into investment distributions.

This script only supports the file provided by [B3](https://www.b3.com.br/pt_br/para-voce).

## Features

- **Data Preprocessing**:
  - Cleans and preprocesses data from fixed income, stock market, and treasury investments.
  - Handles Excel files with investment data.

- **Visualization**:
  - Generates bar charts showing the distribution of investments by year and index.
  - Creates pie charts to display the proportion of investments in fixed income and stock market.

## Requirements

- Python 3.8 or higher
- Required Python libraries:
  - `pandas`
  - `matplotlib`
  - `openpyxl`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/investment-analysis.git
cd investment-analysis
```

2. Create a virtual environment and activate it:

```
python3 -m venv env
source env/bin/activate
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Usage

1. Place your investment data Excel file in the project directory. Ensure the file contains the following sheets:
  - Renda Fixa: Fixed income data
  - Tesouro Direto: Treasury investments
  - Acoes: Stock market data

2. Update the file path in the main function of the scripts:

  `base_xls = "~/path-to-your-excel-file.xlsx"`

3. Run the script:

  `python stock_market_and_fixed_income.py`

4. View the generated visualizations:
  - Bar charts for fixed income and treasury investments.
  - Pie charts showing the distribution of investments.

## File Structure

- `stock_market_and_fixed_income.py` : Processes and visualizes data for fixed income and stock market investments.
- `fixed_income_and_treasures.py`: Handles fixed income and treasury investment data.

## Example Visualizations

### Bar Chart
Displays the distribution of fixed income and treasury investments by year and index.

### Pie Chart
Shows the proportion of investments in fixed income and stock market.