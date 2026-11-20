# Food Delivery Operations Analytics (Beginner Project)

This project analyses a sample food-delivery dataset using **only basic Python, Pandas and NumPy**. No Matplotlib, Seaborn, plotting libraries, or dashboards are used. Results are displayed in the terminal and saved as CSV/text files.

## Requirements
- Python 3
- pandas
- numpy

## Run
1. Install packages: `pip install pandas numpy`
2. Keep `08_food_delivery.csv` in this folder.
3. Run: `python food_delivery_analysis.py`

## Analyses included
- Dataset inspection, missing delivery times and duplicate order IDs
- Order-status counts and percentages
- Average delivery time by city
- Top restaurants by total order value and average order value
- Orders by hour and busiest hour(s)
- Delivery-time statistics by order status
- City cancellation, delay and delivery rates
- NumPy median, sample standard deviation and IQR outlier detection
- Delivery-time bands using project-defined thresholds
- Revenue by city and payment mode
- City and restaurant performance tables
- Automatically generated operational recommendations

## Output
The `outputs/` folder contains CSV tables, cleaned data, a summary report and recommendations.

## Libraries used
- **Python basics:** variables, conditionals, loops, file handling
- **Pandas:** read_csv, DataFrame operations, groupby, value_counts, crosstab, pivot_table, aggregation, sorting, CSV export
- **NumPy:** median, standard deviation, percentile and select

## Limitations
This project uses a sample dataset and describes patterns in these records only. It does not establish causation or represent all food-delivery operations.
