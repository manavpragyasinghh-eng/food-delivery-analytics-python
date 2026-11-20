# Project Results: Food Delivery Operations Analytics\n\nFOOD DELIVERY OPERATIONS ANALYTICS - RESULTS SUMMARY\nTotal orders: 500\nMissing delivery-time records: 7\nDuplicate Order_ID records: 0\n\nStatus percentages:\n              Order_Count  Percentage
Order_Status                         
Delivered             407        81.4
Delayed                47         9.4
Cancelled              46         9.2\n\nAverage delivery time by city:\nCity
Faridabad    35.185714
Delhi        36.043478
Gurugram     36.087719
Noida        37.459677\n\nTop 5 restaurants by total order value:\nRestaurant
Pizza Point    50662.50
Green Bowl     49773.47
Urban Bites    46168.30
Spice Hub      41464.49
Cafe 24        39652.52\n\nAverage order value by restaurant:\nRestaurant
Green Bowl     465.172617
Urban Bites    461.683000
Cafe 24        455.776092
Spice Hub      450.700978
Pizza Point    444.407895\n\nOrders by hour:\nOrder_Hour
8     34
9     34
10    38
11    30
12    16
13    36
14    27
15    30
16    26
17    29
18    38
19    31
20    33
21    37
22    29
23    32\n\nDelivery time by status:\n              count       mean  median   min   max
Order_Status                                      
Cancelled        46  36.521739    38.5  10.0  53.0
Delayed          47  36.191489    35.0  13.0  62.0
Delivered       400  36.122500    35.0  10.0  75.0\n\nCity status rates:\nOrder_Status  Cancelled  Delayed  Delivered  Total_Orders  Cancellation_Rate_%  Status_Delay_Rate_%  Delivered_Rate_%
City                                                                                                                 
Delhi                12       12         95           119            10.084034            10.084034         79.831933
Faridabad             9       11        121           141             6.382979             7.801418         85.815603
Gurugram             13       11         91           115            11.304348             9.565217         79.130435
Noida                12       13        100           125             9.600000            10.400000         80.000000\n\nDelivery median: 36.00\nSample standard deviation: 11.72\nIQR outlier bounds: 4.00 to 68.00\nOutlier count: 2\n\nDelivery bands:\nDelivery_Band
Fast        151
Standard    239
Delayed     103\n\nRevenue pivot:\nPayment_Mode      Card      Cash       UPI      Total
City                                                 
Delhi         18242.29  17373.79  19298.39   54914.47
Faridabad     27959.61  20585.91  12414.03   60959.55
Gurugram      16440.50  21349.48  17616.62   55406.60
Noida         20550.72  16832.78  19057.16   56440.66
Total         83193.12  76141.96  68386.20  227721.28\n\nRecommendations:\n1. Investigate delivery bottlenecks in Noida, which has the highest city-level average delivery time in the available records.\n2. Review cancellation causes and order-confirmation practices in Gurugram, the city with the highest cancellation rate.\n3. Review staffing, dispatch capacity and restaurant preparation coordination in Noida, which has the highest status-based delay rate.\n4. Plan rider and support capacity around hour 10, the busiest order hour in this dataset.\n5. Study practices and menu/order handling at Pizza Point, the restaurant with the highest total order value; do not assume its performance causes other restaurant outcomes.