
import matplotlib.pyplot as plt


COLORS = [
    "#B99AE8",
    "#F4B8CE",
    "#A8DCC0",
    "#FFD6A5",
    "#A9C7F7",
    "#D8C4E8"
]


def create_pie_chart(category_data):
    fig, ax = plt.subplots(figsize=(5, 3.4))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    if category_data.empty or category_data.sum() <= 0:
        ax.text(0.5, 0.5, "Add expenses to see your chart",
                ha="center", va="center", color="#81738F")
        ax.axis("off")
    else:
        ax.pie(
            category_data.values,
            labels=category_data.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=COLORS[:len(category_data)],
            textprops={"fontsize": 8, "color": "#403653"},
            wedgeprops={"edgecolor": "white", "linewidth": 2}
        )
        ax.set_title("Spending by Category", color="#403653", pad=12)

    fig.tight_layout()
    return fig


def create_bar_chart(category_data):
    fig, ax = plt.subplots(figsize=(5, 3.4))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    if category_data.empty:
        ax.text(0.5, 0.5, "No expense data yet",
                ha="center", va="center", color="#81738F")
        ax.axis("off")
    else:
        ax.bar(
            category_data.index,
            category_data.values,
            color=COLORS[:len(category_data)],
            width=0.65
        )
        ax.set_title("Category Comparison", color="#403653")
        ax.set_ylabel("Amount (₹)", color="#403653")
        ax.tick_params(axis="x", labelrotation=25, labelsize=8)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(axis="y", alpha=0.2)
        ax.set_axisbelow(True)

    fig.tight_layout()
    return fig


def create_line_chart(daily_data):
    fig, ax = plt.subplots(figsize=(5, 3.4))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    if daily_data.empty:
        ax.text(0.5, 0.5, "Add expenses to see your trend",
                ha="center", va="center", color="#81738F")
        ax.axis("off")
    else:
        ax.plot(
            daily_data.index,
            daily_data.values,
            color="#A98AD9",
            marker="o",
            linewidth=2.5,
            markersize=5
        )
        ax.fill_between(
            range(len(daily_data)),
            daily_data.values,
            color="#E7D8FF",
            alpha=0.6
        )
        ax.set_xticks(range(len(daily_data)))
        ax.set_xticklabels(
            daily_data.index, rotation=35, ha="right", fontsize=7
        )
        ax.set_title("Daily Spending Trend", color="#403653")
        ax.set_ylabel("Amount (₹)", color="#403653")
        ax.grid(axis="y", alpha=0.2)
        ax.set_axisbelow(True)

    fig.tight_layout()
    return fig
