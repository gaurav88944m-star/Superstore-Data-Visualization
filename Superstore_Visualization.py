
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

df = pd.read_csv(
    "Sample - Superstore (1).csv",
    encoding="cp1252"
)

# 2. Clean data
for column in ["Sales", "Profit", "Quantity"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%m/%d/%Y",
    errors="coerce"
)

df = df.dropna(
    subset=["Sales", "Profit", "Quantity", "Category", "Order Date"]
)

if df.empty:
    raise ValueError("Dataset has no valid rows to visualize.")

# 3. NumPy calculations
sales = df["Sales"].to_numpy()
profit = df["Profit"].to_numpy()

total_sales = np.sum(sales)
total_profit = np.sum(profit)
total_records = len(df)

# 4. Group data
category_sales = df.groupby("Category")["Sales"].sum().sort_values(
    ascending=False
)
category_profit = df.groupby("Category")["Profit"].sum()

monthly_sales = (
    df.assign(Month=df["Order Date"].dt.to_period("M"))
      .groupby("Month")["Sales"]
      .sum()
)

# 5. Professional styling
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "figure.facecolor": "#F3F6FB",
    "axes.facecolor": "white",
    "savefig.facecolor": "#F3F6FB"
})

BLUE = "#4776E6"
TEAL = "#27AE99"
PURPLE = "#8874D8"
ORANGE = "#F0A34A"
DARK = "#24324A"
MUTED = "#6B778C"
GRID = "#E8EDF5"

# 6. Create ONE dashboard window
fig = plt.figure(figsize=(15, 10), facecolor="#F3F6FB")

fig.suptitle(
    "SUPERSTORE  |  SALES ANALYTICS DASHBOARD",
    fontsize=20,
    fontweight="bold",
    color=DARK,
    y=0.975
)

fig.text(
    0.5, 0.943,
    "Business performance overview • Sales, profit and trends",
    ha="center",
    fontsize=10,
    color=MUTED
)

gs = GridSpec(
    3, 2,
    figure=fig,
    height_ratios=[0.75, 2.2, 2.2],
    hspace=0.38,
    wspace=0.22,
    left=0.07,
    right=0.96,
    top=0.89,
    bottom=0.08
)

# 7. KPI cards
kpi_grid = gs[0, :].subgridspec(1, 3, wspace=0.12)

kpis = [
    ("TOTAL SALES", f"${total_sales:,.2f}", BLUE),
    ("TOTAL PROFIT", f"${total_profit:,.2f}", TEAL),
    ("RECORDS ANALYZED", f"{total_records:,}", PURPLE)
]

for i, (label, value, color) in enumerate(kpis):
    ax = fig.add_subplot(kpi_grid[0, i])
    ax.set_facecolor("white")

    for spine in ax.spines.values():
        spine.set_color("#E1E7F0")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    ax.text(
        0.06, 0.70, label,
        transform=ax.transAxes,
        fontsize=9,
        color=MUTED,
        fontweight="bold"
    )

    ax.text(
        0.06, 0.28, value,
        transform=ax.transAxes,
        fontsize=17 if i < 2 else 21,
        color=color,
        fontweight="bold"
    )

    ax.axhline(
        0.04, xmin=0.06, xmax=0.94,
        color=color, linewidth=3
    )

# 8. Chart 1: Sales by category
ax1 = fig.add_subplot(gs[1, 0])

categories = category_sales.index.to_list()
sales_values = category_sales.to_numpy()

bars = ax1.bar(
    categories,
    sales_values,
    color=[BLUE, TEAL, PURPLE][:len(categories)],
    width=0.62
)

ax1.set_title("Sales by Product Category", loc="left", pad=12)
ax1.set_ylabel("Sales ($)")
ax1.set_ylim(0, max(sales_values) * 1.17)
ax1.ticklabel_format(axis="y", style="plain")
ax1.grid(axis="y", color=GRID)
ax1.set_axisbelow(True)
ax1.grid(axis="x", visible=False)

for bar in bars:
    height = bar.get_height()
    ax1.annotate(
        f"${height:,.0f}",
        (bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, 5),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        fontweight="bold",
        color=DARK
    )

# 9. Chart 2: Profit by category
ax2 = fig.add_subplot(gs[1, 1])

profit_categories = category_profit.index.to_list()
profit_values = category_profit.reindex(profit_categories).to_numpy()

profit_colors = [
    TEAL if value >= 0 else "#E45B65"
    for value in profit_values
]

bars2 = ax2.bar(
    profit_categories,
    profit_values,
    color=profit_colors,
    width=0.62
)

ax2.set_title("Profit by Product Category", loc="left", pad=12)
ax2.set_ylabel("Profit ($)")
ax2.axhline(0, color=MUTED, linewidth=0.8)
ax2.grid(axis="y", color=GRID)
ax2.set_axisbelow(True)
ax2.grid(axis="x", visible=False)

for bar in bars2:
    height = bar.get_height()
    offset = 4 if height >= 0 else -13

    ax2.annotate(
        f"${height:,.0f}",
        (bar.get_x() + bar.get_width() / 2, height),
        xytext=(0, offset),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        fontweight="bold",
        color=DARK
    )

# 10. Chart 3: Monthly sales trend
ax3 = fig.add_subplot(gs[2, 0])

month_values = monthly_sales.to_numpy()
month_labels = monthly_sales.index.astype(str).to_list()
x = np.arange(len(month_values))

ax3.plot(
    x,
    month_values,
    color=BLUE,
    linewidth=2.2,
    marker="o",
    markersize=3.5
)

ax3.fill_between(
    x, month_values, 0,
    color=BLUE,
    alpha=0.10
)

ax3.set_title("Monthly Sales Trend", loc="left", pad=12)
ax3.set_ylabel("Sales ($)")
ax3.set_xlabel("Order month")
ax3.set_ylim(bottom=0)
ax3.set_xticks(x[::4])
ax3.set_xticklabels(month_labels[::4], rotation=30, ha="right")
ax3.grid(axis="y", color=GRID)
ax3.set_axisbelow(True)
ax3.grid(axis="x", visible=False)

# 11. Chart 4: Sales contribution donut chart
ax4 = fig.add_subplot(gs[2, 1])

pie_colors = [BLUE, TEAL, PURPLE][:len(categories)]

wedges, _, _ = ax4.pie(
    sales_values,
    labels=None,
    colors=pie_colors,
    startangle=90,
    autopct="%1.1f%%",
    pctdistance=0.78,
    wedgeprops={
        "width": 0.38,
        "edgecolor": "white",
        "linewidth": 2
    },
    textprops={
        "fontsize": 10,
        "fontweight": "bold"
    }
)

ax4.set_title("Sales Contribution", loc="left", pad=12)

ax4.text(
    0, 0,
    "TOTAL\nSALES",
    ha="center",
    va="center",
    fontsize=11,
    fontweight="bold",
    color=DARK
)

ax4.legend(
    wedges,
    categories,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.08),
    ncol=min(3, len(categories)),
    frameon=False,
    fontsize=9
)

# 12. Clean up axes and display the entire dashboard
for ax in [ax1, ax2, ax3]:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)

fig.text(
    0.96, 0.025,
    "Built with NumPy • Pandas • Matplotlib",
    ha="right",
    fontsize=8,
    color=MUTED
)

# Only ONE show() call: all charts appear in one GUI window
plt.show()

print("\nDashboard closed.")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print("Dashboard completed successfully!")
