import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# %% read data
df19 = pd.read_csv("2019data1.csv", parse_dates=["Date"])
df22 = pd.read_csv("2022data1.csv", parse_dates=["Date and time"])

# %% 2019 totals (bus + metro only)
date19 = pd.DatetimeIndex(df19["Date"])

bus_peak19 = np.array(df19["Bus pax number peak"])
bus_off19 = np.array(df19["Bus pax number offpeak"])
metro_peak19 = np.array(df19["Metro pax number peak"])
metro_off19 = np.array(df19["Metro pax number offpeak"])

pax19 = bus_peak19 + bus_off19 + metro_peak19 + metro_off19

day19 = np.array(date19.dayofyear)
wday19 = np.array(date19.weekday)

# %% 2022 data: extra columns and daily totals
df22["Date_only"] = df22["Date and time"].dt.date

dt22 = pd.DatetimeIndex(df22["Date and time"])
month22 = np.array(dt22.month)
wday22_all = np.array(dt22.weekday)
hour22 = np.array(dt22.hour)

mode22 = np.array(df22["Mode"])
dist22 = np.array(df22["Distance"])
price22 = np.array(df22["Price"])

df22_daily = (
    df22.groupby("Date_only")
    .size()
    .reset_index(name="count")
)
date_daily22 = pd.to_datetime(df22_daily["Date_only"])

day22 = np.array(pd.DatetimeIndex(date_daily22).dayofyear)
wday22 = np.array(pd.DatetimeIndex(date_daily22).weekday)
pax22_sample = np.array(df22_daily["count"])

# %% statistical scaling for 2022 totals (single factor)
total19 = np.sum(pax19)
total22_sample = np.sum(pax22_sample)

scale22 = total19 / total22_sample

pax22 = pax22_sample * scale22

# %% Fourier preparation
x19 = day19.astype(float)
y19 = pax19.astype(float)

x22 = day22.astype(float)
y22 = pax22.astype(float)

n19 = len(x19)
n22 = len(x22)

xmin19 = np.min(x19)
xmax19 = np.max(x19)
t19 = xmax19 - xmin19

xmin22 = np.min(x22)
xmax22 = np.max(x22)
t22 = xmax22 - xmin22

# %% Fourier coefficients for 2019
a19 = np.zeros(n19)
b19 = np.zeros(n19)

for k in range(n19):
    ang = 2.0 * np.pi * k * (x19 - xmin19) / t19
    if k == 0:
        a19[k] = (1.0 / n19) * np.sum(y19 * np.cos(ang))
        b19[k] = 0.0
    else:
        a19[k] = (2.0 / n19) * np.sum(y19 * np.cos(ang))
        b19[k] = (2.0 / n19) * np.sum(y19 * np.sin(ang))

# %% Fourier coefficients for 2022
a22 = np.zeros(n22)
b22 = np.zeros(n22)

for k in range(n22):
    ang = 2.0 * np.pi * k * (x22 - xmin22) / t22
    if k == 0:
        a22[k] = (1.0 / n22) * np.sum(y22 * np.cos(ang))
        b22[k] = 0.0
    else:
        a22[k] = (2.0 / n22) * np.sum(y22 * np.cos(ang))
        b22[k] = (2.0 / n22) * np.sum(y22 * np.sin(ang))

# %% build 8-term Fourier curves
x_plot = np.arange(1, 366, dtype=float)

y_smooth19 = np.zeros(365)
y_smooth22 = np.zeros(365)

n_terms = 8

for i in range(365):
    xx = x_plot[i]

    s1 = a19[0]
    s2 = a22[0]

    for k in range(1, n_terms):
        ang1 = 2.0 * np.pi * k * (xx - xmin19) / t19
        ang2 = 2.0 * np.pi * k * (xx - xmin22) / t22
        s1 = s1 + a19[k] * np.cos(ang1) + b19[k] * np.sin(ang1)
        s2 = s2 + a22[k] * np.cos(ang2) + b22[k] * np.sin(ang2)

    y_smooth19[i] = s1
    y_smooth22[i] = s2

# %% weekday averages (for Figure 2)
mean19 = np.zeros(7)
mean22 = np.zeros(7)

for i in range(7):
    mean19[i] = np.mean(pax19[wday19 == i])
    mean22[i] = np.mean(pax22[wday22 == i])

# %% extra task: revenue fractions X, Y, Z
weekday22 = wday22_all < 5
weekend22 = wday22_all >= 5

peak = (
    ((hour22 >= 7) & (hour22 <= 9))
    | ((hour22 >= 16) & (hour22 <= 18))
)
peak_weekday = weekday22 & peak
off_weekday = weekday22 & (~peak)

rev_peak = np.sum(price22[peak_weekday])
rev_off = np.sum(price22[off_weekday])
rev_weekend = np.sum(price22[weekend22])

total_rev = rev_peak + rev_off + rev_weekend

x_val = rev_peak / total_rev
y_val = rev_off / total_rev
z_val = rev_weekend / total_rev

print("X =", x_val)
print("Y =", y_val)
print("Z =", z_val)

# %% 2019 peak / off-peak / weekend totals
weekend19 = wday19 >= 5
weekday19 = wday19 < 5

pax_peak19 = bus_peak19 + metro_peak19
pax_off19 = bus_off19 + metro_off19

total_peak19 = np.sum(pax_peak19[weekday19])
total_off19 = np.sum(pax_off19[weekday19])
total_weekend19 = np.sum(pax19[weekend19])

# %% 2022 peak / off-peak / weekend estimates (scaled)
total_peak22_sample = np.sum(peak_weekday)
total_off22_sample = np.sum(off_weekday)
total_weekend22_sample = np.sum(weekend22)

total_peak22 = total_peak22_sample * scale22
total_off22 = total_off22_sample * scale22
total_weekend22 = total_weekend22_sample * scale22

vals19 = np.array([total_peak19, total_off19, total_weekend19]) / 1e6
vals22 = np.array([total_peak22, total_off22, total_weekend22]) / 1e6

# %% Figure 1 – single y-axis, same units
plt.figure(1, dpi=130, figsize=(8, 4))
ax1 = plt.gca()

ax1.scatter(
    day19,
    pax19 / 1e6,
    s=8,
    color="cornflowerblue",
    alpha=0.6,
    label="2019 daily passengers",
)
ax1.plot(
    x_plot,
    y_smooth19 / 1e6,
    color="darkred",
    linewidth=2,
    label="2019 Fourier (8-term)",
)

ax1.scatter(
    day22,
    pax22 / 1e6,
    s=8,
    color="darkorange",
    alpha=0.6,
    label="2022 daily passengers (estimated)",
)
ax1.plot(
    x_plot,
    y_smooth22 / 1e6,
    color="seagreen",
    linewidth=2,
    label="2022 Fourier (8-term, estimated)",
)

ax1.set_xlabel("Day of Year (1–365)")
ax1.set_ylabel("Total daily passengers (millions)")

plt.title(
    "Figure 1: Daily Passenger Totals and 8-Term Fourier – "
    "ID: 24127511"
)

plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()

# %% Figure 2 – weekday averages (log scale)
plt.figure(2, dpi=130, figsize=(7, 4))
ax2 = plt.gca()

xpos = np.arange(7)
w = 0.35
labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

plt.bar(
    xpos - w / 2,
    mean19,
    w,
    label="2019",
    color="royalblue",
)
plt.bar(
    xpos + w / 2,
    mean22,
    w,
    label="2022 (estimated)",
    color="peru",
)

plt.xticks(xpos, labels)
plt.yscale("log")
plt.xlabel("Weekday")
plt.ylabel("Average passengers (log scale)")
plt.title("Figure 2: Average Weekday Totals – ID: 24127511")

txt = (
    "X = " + str(round(x_val, 3)) + " (peak revenue)\n"
    "Y = " + str(round(y_val, 3)) + " (off-peak workdays)\n"
    "Z = " + str(round(z_val, 3)) + " (weekend revenue)"
)

ax2.text(
    0.02,
    0.95,
    txt,
    transform=ax2.transAxes,
    fontsize=9,
    va="top",
    ha="left",
    bbox=dict(facecolor="white", alpha=0.9),
)

plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()

# %% Figure 3 – regression
mask_metro = mode22 == "Metro"
dist_metro = dist22[mask_metro]
price_metro = price22[mask_metro]

n = len(dist_metro)
sx = np.sum(dist_metro)
sy = np.sum(price_metro)
sxx = np.sum(dist_metro * dist_metro)
sxy = np.sum(dist_metro * price_metro)

den = n * sxx - sx * sx
a = (n * sxy - sx * sy) / den
b = (sxx * sy - sx * sxy) / den

x_line = np.linspace(
    np.min(dist_metro),
    np.max(dist_metro),
    200,
)
y_line = a * x_line + b

plt.figure(3, dpi=130, figsize=(7, 4))
ax3 = plt.gca()

plt.scatter(
    dist_metro,
    price_metro,
    s=10,
    color="teal",
    label="Metro journeys 2022",
)
plt.plot(
    x_line,
    y_line,
    color="crimson",
    linewidth=2,
    label="Regression line",
)

plt.xlabel("Distance (km)")
plt.ylabel("Price (EUR)")
plt.title("Figure 3: Metro Ticket Price vs Distance – ID: 24127511")

eq = (
    "Price = " + str(round(a, 3))
    + " × Distance + " + str(round(b, 3))
)

ax3.text(
    0.02,
    0.95,
    eq,
    transform=ax3.transAxes,
    fontsize=9,
    va="top",
    ha="left",
)

plt.legend(loc="lower right", fontsize=8)
plt.tight_layout()

# %% Figure 4 – peak / off-peak / weekends
plt.figure(4, dpi=130, figsize=(7, 4))
ax4 = plt.gca()

cats = ["Peak (workdays)", "Off-peak (workdays)", "Weekends"]
xpos2 = np.arange(3)
w2 = 0.35

plt.bar(
    xpos2 - w2 / 2,
    vals19,
    w2,
    color="cornflowerblue",
    label="2019 journeys (millions)",
)
plt.bar(
    xpos2 + w2 / 2,
    vals22,
    w2,
    color="orange",
    label="2022 journeys (estimated, millions)",
)

plt.xticks(xpos2, cats)
plt.ylabel("Passengers / journeys (millions)")
plt.xlabel("Category")
plt.title(
    "Figure 4: Peak, Off-Peak and Weekend Journeys – ID: 24127511"
)

txt2 = (
    "X = " + str(round(x_val, 3)) + " (peak revenue)\n"
    "Y = " + str(round(y_val, 3)) + " (off-peak workdays)\n"
    "Z = " + str(round(z_val, 3)) + " (weekend revenue)"
)

ax4.text(
    0.02,
    0.95,
    txt2,
    transform=ax4.transAxes,
    fontsize=9,
    va="top",
    ha="left",
    bbox=dict(facecolor="white", alpha=0.9),
)

plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()

# %% New Figure: Bus passengers per day in July 2019 (no red line)
plt.figure(5, dpi=130, figsize=(12, 6))

july19 = df19[(df19["Date"].dt.year == 2019) & (df19["Date"].dt.month == 7)].copy()
july19 = july19.sort_values("Date")
july19["Day"] = july19["Date"].dt.day

bus_total_july = july19["Bus pax number peak"] + july19["Bus pax number offpeak"]

plt.bar(july19["Day"], bus_total_july, color='royalblue', alpha=0.8, edgecolor='navy', width=0.7)

plt.title("Bus Passengers per Day – July 2019 ID: 24127511")
plt.xlabel("Day of July")
plt.ylabel("Total Bus Passengers (peak + off-peak)")
plt.xticks(range(1, 32))
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()

# %% show plots
plt.show()