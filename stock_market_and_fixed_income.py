import configparser
import os
import pandas as pd
import matplotlib.pyplot as plt

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

def read_data(file_path, sheet_name, index_col=4):
    """Reads data from an Excel sheet."""
    return pd.read_excel(
        file_path,
        engine="openpyxl",
        index_col=index_col,
        parse_dates=True,
        date_format="DD/MM/YYYY",
        sheet_name=sheet_name,
    )


def preprocess_fixed_income_and_treasures(fixed_income, treasures):
    """Preprocesses and combines fixed income and treasures data."""
    combined_fixed_income = pd.concat([fixed_income, treasures])
    filtered_by_index = combined_fixed_income.loc[
        combined_fixed_income.index.isin(["PREFIXADO", "DI", "IPCA", "prefixado"])
    ]
    updated_value_from_fixed_income = filtered_by_index[["Valor Atualizado CURVA"]]
    updated_value_from_fixed_income["Valor Atualizado CURVA"] = (
        updated_value_from_fixed_income["Valor Atualizado CURVA"]
        .replace("[\$,]", "", regex=True)
        .astype(float)
    )
    return updated_value_from_fixed_income


def preprocess_stock_market(stock_market):
    """Preprocesses stock market data."""
    filtered_by_quantity = stock_market[stock_market["Quantidade"] > 0]
    updated_value_from_stock_market = filtered_by_quantity[["Valor Atualizado"]]
    updated_value_from_stock_market["Valor Atualizado"] = (
        updated_value_from_stock_market["Valor Atualizado"]
        .replace("[\$,]", "", regex=True)
        .astype(float)
    )
    return updated_value_from_stock_market


def format_percentage_and_value(pct, allvals):
    """Formats the percentage and absolute value for the pie chart."""
    absolute = int(pct / 100.0 * sum(allvals))
    return f"{pct:.1f}%\n({absolute:,})"


def create_pie_chart(fixed_income_total, stock_market_total):
    """Creates and displays a pie chart."""
    # Create a DataFrame for the pie chart
    pie_data = pd.DataFrame(
        {
            "Category": ["Fixed Income", "Stock Market"],
            "Value": [fixed_income_total, stock_market_total],
        }
    )

    # Create the pie chart
    pie_data.set_index("Category").plot.pie(
        y="Value",
        autopct=lambda pct: format_percentage_and_value(pct, pie_data["Value"]),
        startangle=90,
        legend=False,
    )
    plt.title("Distribuicao dos investimentos")
    plt.ylabel("")  # Hide the y-label
    plt.show()


def main():
    """Main function to execute the script."""
    # File path
    # base_xls = "~/Downloads/updated-all-b3.xlsx"
    base_xls = os.path.expanduser(config["Paths"]["base_xls"])

    # Read data
    fixed_income = read_data(base_xls, sheet_name="Renda Fixa")
    treasures = read_data(base_xls, sheet_name="Tesouro Direto")
    stock_market = read_data(base_xls, sheet_name="Acoes")

    # Preprocess data
    updated_value_from_fixed_income = preprocess_fixed_income_and_treasures(
        fixed_income, treasures
    )
    updated_value_from_stock_market = preprocess_stock_market(stock_market)

    # Sum the values for each category
    fixed_income_total = updated_value_from_fixed_income["Valor Atualizado CURVA"].sum()
    stock_market_total = updated_value_from_stock_market["Valor Atualizado"].sum()

    # Create and display the pie chart
    create_pie_chart(fixed_income_total, stock_market_total)


if __name__ == "__main__":
    main()
