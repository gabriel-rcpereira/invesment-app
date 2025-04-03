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


def preprocess_data(data, columns_to_keep, date_column, value_column):
    """Preprocesses the data by filtering columns, converting types, and extracting the year."""
    # Select specific columns
    data = data[columns_to_keep]

    # Convert value column to numeric
    data[value_column] = (
        data[value_column].replace("[\$,]", "", regex=True).astype(float)
    )

    # Ensure date column is in datetime format
    data[date_column] = pd.to_datetime(data[date_column], format="%d/%m/%Y")

    # Extract the year from the date column
    data["Year"] = data[date_column].dt.year

    return data


def plot_data(grouped_data):
    """Plots the bar chart and annotates it with values and percentages."""
    # Plot the bar chart
    ax = grouped_data.plot(kind="bar", stacked=True)
    plt.title("Valor Atualizado por Ano e Indexador")
    plt.xlabel("Year")
    plt.ylabel("Valor Atualizado")
    plt.legend(title="Index")

    # Annotate each bar with the value and percentage relative to the total of each bar
    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            if height > 0:
                # Get the total value for the specific bar (year)
                year_index = int(
                    bar.get_x() + 0.5
                )  # Convert x-coordinate to the corresponding index
                year_total = grouped_data.iloc[year_index].sum()
                percentage = (height / year_total) * 100
                # Annotate the bar with value and percentage
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 2,
                    f"{height:,.2f}\n({percentage:.1f}%)",
                    ha="center",
                    va="center",
                    fontsize=8,
                )

    # Add the total value to the plot
    total_value = grouped_data.sum().sum()
    plt.text(
        1.03,
        0.95,
        f"Total: {total_value:,.2f}",
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=dict(facecolor="white", alpha=0.5),
    )

    plt.show()


def main():
    """Main function to execute the script."""
    # File path
    base_xls = os.path.expanduser(config["Paths"]["base_xls"])

    # Read data
    fixed_income = read_data(base_xls, sheet_name="Renda Fixa")
    treasures = read_data(base_xls, sheet_name="Tesouro Direto")

    # Concatenate the fixed income and treasures data
    combined_data = pd.concat([fixed_income, treasures])

    # Filter by index column
    filtered_by_index = combined_data.loc[
        combined_data.index.isin(["PREFIXADO", "DI", "IPCA", "prefixado"])
    ]

    # Preprocess the data
    only_a_few_columns = preprocess_data(
        filtered_by_index,
        columns_to_keep=["Vencimento", "Valor Atualizado CURVA"],
        date_column="Vencimento",
        value_column="Valor Atualizado CURVA",
    )

    # Group by 'Year' and index, then sum 'Valor Atualizado CURVA'
    grouped_data = (
        only_a_few_columns.groupby(["Year", only_a_few_columns.index])[
            "Valor Atualizado CURVA"
        ]
        .sum()
        .unstack()
    )

    # Plot the data
    plot_data(grouped_data)


if __name__ == "__main__":
    main()
