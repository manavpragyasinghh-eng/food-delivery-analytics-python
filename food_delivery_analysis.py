from pathlib import Path
import pandas as pd
import numpy as np

# ----------------------------- Setup ---------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "08_food_delivery.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------- Task 109: Load and inspect --------------------------
df = pd.read_csv(DATA_FILE)
print("\\nTASK 109: DATASET INSPECTION")
print("Shape:", df.shape)
print("\\nFirst 5 rows:\\n", df.head())
print("\\nColumn names:", df.columns.tolist())
print("\\nData types:\\n", df.dtypes)
print("\\nDataset information:")
df.info()

# ---------------- Task 110: Missing delivery times -------------------
missing_delivery = df["Delivery_Time_Min"].isna().sum()
print("\\nTASK 110: MISSING DELIVERY TIMES:", missing_delivery)

# Do not fabricate delivery durations. Keep all orders for order/revenue
# analysis, but exclude missing delivery-time rows from time-based metrics.
df_time = df.dropna(subset=["Delivery_Time_Min"]).copy()
print("Rows retained for delivery-time analysis:", len(df_time))

# ---------------- Task 111: Duplicate Order_ID ----------------------
duplicate_ids = df["Order_ID"].duplicated().sum()
print("\\nTASK 111: DUPLICATE Order_ID COUNT:", duplicate_ids)
if duplicate_ids:
    df = df.drop_duplicates(subset="Order_ID", keep="first").copy()
    df_time = df.dropna(subset=["Delivery_Time_Min"]).copy()

# ---------------- Task 112: Orders and status percentages ----------
total_orders = len(df)
status_counts = df["Order_Status"].value_counts()
status_percentages = df["Order_Status"].value_counts(normalize=True).mul(100)
status_summary = pd.DataFrame({
    "Order_Count": status_counts,
    "Percentage": status_percentages
})
print("\\nTASK 112: TOTAL ORDERS:", total_orders)
print(status_summary)
status_summary.to_csv(OUTPUT_DIR/"order_status_summary.csv")

# ---------------- Task 113: Average delivery time by city ----------
city_avg_delivery = df_time.groupby("City")["Delivery_Time_Min"].mean().sort_values()
print("\\nTASK 113: AVERAGE DELIVERY TIME BY CITY")
print(city_avg_delivery)
city_avg_delivery.to_csv(OUTPUT_DIR/"average_delivery_time_by_city.csv")

# ---------------- Task 114: Top 5 restaurants by order value ------
top_restaurants = df.groupby("Restaurant")["Order_Value"].sum().sort_values(ascending=False).head(5)
print("\\nTASK 114: TOP 5 RESTAURANTS BY TOTAL ORDER VALUE")
print(top_restaurants)
top_restaurants.to_csv(OUTPUT_DIR/"top_5_restaurants_total_value.csv")

# ---------------- Task 115: Average order value by restaurant ------
restaurant_avg = df.groupby("Restaurant")["Order_Value"].mean().sort_values(ascending=False)
print("\\nTASK 115: AVERAGE ORDER VALUE BY RESTAURANT")
print(restaurant_avg)
restaurant_avg.to_csv(OUTPUT_DIR/"average_order_value_by_restaurant.csv")

# ---------------- Task 116: Peak ordering hours --------------------
peak_hours = df["Order_Hour"].value_counts().sort_index()
peak_hour_rank = df["Order_Hour"].value_counts().sort_values(ascending=False)
print("\\nTASK 116: ORDERS BY HOUR")
print(peak_hours)
print("Highest-volume hour(s):", peak_hour_rank[peak_hour_rank == peak_hour_rank.max()].index.tolist())
peak_hours.to_csv(OUTPUT_DIR/"orders_by_hour.csv")

# ---------------- Task 117: Delivery time by status ---------------
status_delivery = df_time.groupby("Order_Status")["Delivery_Time_Min"].agg(
    ["count", "mean", "median", "min", "max"]
)
print("\\nTASK 117: DELIVERY TIME BY ORDER STATUS (known times only)")
print(status_delivery)
status_delivery.to_csv(OUTPUT_DIR/"delivery_time_by_status.csv")

# ---------------- Task 118: Cancellation and delay rates by city ---
city_status = pd.crosstab(df["City"], df["Order_Status"])
city_status["Total_Orders"] = city_status.sum(axis=1)
city_status["Cancellation_Rate_%"] = city_status.get("Cancelled", 0) / city_status["Total_Orders"] * 100
city_status["Status_Delay_Rate_%"] = city_status.get("Delayed", 0) / city_status["Total_Orders"] * 100
city_status["Delivered_Rate_%"] = city_status.get("Delivered", 0) / city_status["Total_Orders"] * 100
print("\\nTASK 118: CITY CANCELLATION AND STATUS-DELAY RATES")
print(city_status)
city_status.to_csv(OUTPUT_DIR/"city_cancellation_delay_rates.csv")

# ---------------- Task 119: NumPy median and standard deviation ----
delivery_values = df_time["Delivery_Time_Min"].to_numpy()
delivery_median = np.median(delivery_values)
delivery_std = np.std(delivery_values, ddof=1)  # sample standard deviation
print("\\nTASK 119: MEDIAN DELIVERY TIME:", delivery_median)
print("Sample standard deviation:", delivery_std)

# ---------------- Task 120: IQR outlier detection ------------------
q1 = np.percentile(delivery_values, 25)
q3 = np.percentile(delivery_values, 75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = df_time[(df_time["Delivery_Time_Min"] < lower_bound) |
                   (df_time["Delivery_Time_Min"] > upper_bound)]
print("\\nTASK 120: IQR OUTLIER ANALYSIS")
print(f"Q1={q1:.2f}, Q3={q3:.2f}, IQR={iqr:.2f}")
print(f"Lower bound={lower_bound:.2f}, upper bound={upper_bound:.2f}")
print("Outlier count:", len(outliers))
outliers.to_csv(OUTPUT_DIR/"delivery_time_outliers_iqr.csv", index=False)

# ---------------- Task 121: Delivery time bands ---------------------
# Thresholds are project-defined: Fast <= 30, Standard 31-45, Delayed > 45 min.
conditions = [
    df_time["Delivery_Time_Min"] <= 30,
    df_time["Delivery_Time_Min"].between(31, 45),
    df_time["Delivery_Time_Min"] > 45
]
labels = ["Fast", "Standard", "Delayed"]
df_time["Delivery_Band"] = np.select(conditions, labels, default="Unclassified")
band_summary = df_time["Delivery_Band"].value_counts().reindex(labels, fill_value=0)
print("\\nTASK 121: DELIVERY TIME BANDS")
print(band_summary)
band_summary.to_csv(OUTPUT_DIR/"delivery_time_bands.csv")

# ---------------- Task 122: Revenue by city and payment mode -------
revenue_pivot = pd.pivot_table(
    df, values="Order_Value", index="City", columns="Payment_Mode",
    aggfunc="sum", fill_value=0, margins=True, margins_name="Total"
)
print("\\nTASK 122: REVENUE BY CITY AND PAYMENT MODE")
print(revenue_pivot)
revenue_pivot.to_csv(OUTPUT_DIR/"revenue_by_city_payment_mode.csv")

# ---------------- Optional additional analyses ----------------------
city_performance = df.groupby("City").agg(
    Total_Orders=("Order_ID", "count"),
    Total_Revenue=("Order_Value", "sum"),
    Average_Order_Value=("Order_Value", "mean"),
    Average_Distance_km=("Distance_km", "mean")
)
city_performance = city_performance.join(city_avg_delivery.rename("Average_Delivery_Min"))
city_performance = city_performance.join(city_status[["Cancellation_Rate_%", "Status_Delay_Rate_%", "Delivered_Rate_%"]])
city_performance.sort_values("Total_Orders", ascending=False).to_csv(OUTPUT_DIR/"city_performance.csv")

restaurant_stats = df.groupby("Restaurant").agg(
    Orders=("Order_ID", "count"),
    Total_Order_Value=("Order_Value", "sum"),
    Average_Order_Value=("Order_Value", "mean")
).sort_values("Total_Order_Value", ascending=False)
restaurant_stats.to_csv(OUTPUT_DIR/"restaurant_performance.csv")

# Save dataset copy with delivery band attached for time records.
df_time.to_csv(OUTPUT_DIR/"delivery_times_cleaned_with_bands.csv", index=False)

# ---------------- Task 123: Recommendations ------------------------
# Generated recommendation templates are data-informed; interpret before presenting.
recommendations = []
slowest_city = city_avg_delivery.idxmax() if not city_avg_delivery.empty else "N/A"
highest_cancel_city = city_status["Cancellation_Rate_%"].idxmax() if not city_status.empty else "N/A"
highest_status_delay_city = city_status["Status_Delay_Rate_%"].idxmax() if not city_status.empty else "N/A"
peak_hours_text = ", ".join(map(str, peak_hour_rank[peak_hour_rank == peak_hour_rank.max()].index.tolist())) if not peak_hour_rank.empty else "N/A"
top_restaurant_name = top_restaurants.index[0] if not top_restaurants.empty else "N/A"
recommendations.extend([
    f"Investigate delivery bottlenecks in {slowest_city}, which has the highest city-level average delivery time in the available records.",
    f"Review cancellation causes and order-confirmation practices in {highest_cancel_city}, the city with the highest cancellation rate.",
    f"Review staffing, dispatch capacity and restaurant preparation coordination in {highest_status_delay_city}, which has the highest status-based delay rate.",
    f"Plan rider and support capacity around hour(s) {peak_hours_text}, the busiest order hour(s) in this dataset.",
    f"Study practices and menu/order handling at {top_restaurant_name}, the restaurant with the highest total order value; do not assume its performance causes other restaurant outcomes."
])
with open(OUTPUT_DIR/"recommendations.txt", "w", encoding="utf-8") as f:
    f.write("TASK 123: FIVE OPERATIONAL RECOMMENDATIONS\\n\\n")
    for i, rec in enumerate(recommendations, 1):
        f.write(f"{i}. {rec}\\n")

# ---------------- Summary report -------------------------------------
with open(OUTPUT_DIR/"analysis_summary.txt", "w", encoding="utf-8") as f:
    f.write("FOOD DELIVERY OPERATIONS ANALYTICS - RESULTS SUMMARY\\n")
    f.write(f"Total orders: {total_orders}\\n")
    f.write(f"Missing delivery-time records: {missing_delivery}\\n")
    f.write(f"Duplicate Order_ID records: {duplicate_ids}\\n\\n")
    f.write("Status percentages:\\n" + status_summary.to_string() + "\\n\\n")
    f.write("Average delivery time by city:\\n" + city_avg_delivery.to_string() + "\\n\\n")
    f.write("Top 5 restaurants by total order value:\\n" + top_restaurants.to_string() + "\\n\\n")
    f.write("Average order value by restaurant:\\n" + restaurant_avg.to_string() + "\\n\\n")
    f.write("Orders by hour:\\n" + peak_hours.to_string() + "\\n\\n")
    f.write("Delivery time by status:\\n" + status_delivery.to_string() + "\\n\\n")
    f.write("City status rates:\\n" + city_status.to_string() + "\\n\\n")
    f.write(f"Delivery median: {delivery_median:.2f}\\nSample standard deviation: {delivery_std:.2f}\\n")
    f.write(f"IQR outlier bounds: {lower_bound:.2f} to {upper_bound:.2f}\\nOutlier count: {len(outliers)}\\n\\n")
    f.write("Delivery bands:\\n" + band_summary.to_string() + "\\n\\n")
    f.write("Revenue pivot:\\n" + revenue_pivot.to_string() + "\\n\\n")
    f.write("Recommendations:\\n" + "\\n".join(f"{i}. {r}" for i, r in enumerate(recommendations, 1)))

print("\\nTASK 123: RECOMMENDATIONS")
for i, recommendation in enumerate(recommendations, 1):
    print(f"{i}. {recommendation}")

print("\\nAnalysis complete. Check the outputs/ folder.")
