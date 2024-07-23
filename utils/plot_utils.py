import pandas as pd
from scipy.interpolate import make_interp_spline


def load_csv(file):
    return pd.read_csv(file, index_col=0, parse_dates=True).fillna(0).astype(int)


def plot_smooth(ax, data, y_label):
    dates = data.index
    x = pd.date_range(dates.min(), dates.max(), freq='D')
    spline = make_interp_spline(dates, data, k=1)
    smooth = spline(x)

    ax.plot(x, smooth, 'purple')
    plot_labeled_points(ax, data)


def plot_line(ax, data, y_label, color='purple'):
    ax.plot(data, color)
    ax.set_ylabel(y_label.title())
    plot_labeled_points(ax, data)


def plot_labeled_points(ax, data):
    dates = data.index
    for date in dates:
        y = data.loc[date]
        if y==0: 
            continue
        text = f"{y}"
        ax.text(date, y, s=text, ha='center', va='center', backgroundcolor='w')
    ax.set_xticks(dates, labels=dates.strftime('%B %d'), rotation=45, ha='right')