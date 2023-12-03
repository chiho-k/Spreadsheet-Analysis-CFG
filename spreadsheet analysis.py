import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sales = []
expenditure = []
profit = []
data = []

with open("sales.csv", "r") as file:
    spreadsheetDict = csv.DictReader(file)
    # Make lists containing monthly sales, expenditure and profit (sales-expenditure)
    for row in spreadsheetDict:
        sales.append(int(row["sales"]))
        expenditure.append(int(row["expenditure"]))
        monthlyProfit = int(row["sales"])-int(row["expenditure"])
        profit.append(monthlyProfit)

print("List of sales from each month:", sales, "\n")

# Takes a list and calculates percentage change from one month to the next, returned as a list of percentages
def percentageCalculator(list):
    percentChangeList = [0,]
    x = range(1, 12)
    for n in x:
        percentChange = int(np.round((list[n] - list[n - 1]) / list[n] * 100, 0)) # (e.g. (sales for feb - sales for jan)/sales for feb * 100)
        percentChangeList.append(percentChange)
    return percentChangeList
salesPercentChange = percentageCalculator(sales)
expenditurePercentChange = percentageCalculator(expenditure)
profitPercentChange = percentageCalculator(profit)

# Adding new columns to dictionary data extracted from csv
with open("sales.csv", "r") as file:
    spreadsheetDict = csv.DictReader(file)
    n = 0
    for row in spreadsheetDict:
        row["profit"] = str(profit[n])
        row["% change sales"] = salesPercentChange[n]
        row["% change expenditure"] = expenditurePercentChange[n]
        row["% change profit"] = profitPercentChange[n]
        data.append(row)
        n += 1

# Field names used to add new column names
fieldnames = ["year", "month", "sales", "expenditure", "profit", "% change sales", "% change expenditure", "% change profit"]
# Writing new columns into csv file: profit, %change sales, %change expenditure, %change profit
with open("sales.csv", "w+") as file:
    newSpreadsheet = csv.DictWriter(file, fieldnames = fieldnames)
    newSpreadsheet.writeheader()
    newSpreadsheet.writerows(data)

# Calculating total in entire year
totalSale = 0
def totalCalculator(list):
    total = 0
    for monthlyValue in list:
        total += monthlyValue
    return total
totalSale = totalCalculator(sales)
totalExpenditure = totalCalculator(expenditure)
totalProfit = totalCalculator(profit)

# Calculating monthly average by dividing yearly total by 12
averageSale = int(np.round(totalSale/12,0))
averageExpenditure = int(np.round(totalExpenditure/12, 0))
averageProfit = int(np.round(totalProfit/12,0))

# Finding minimum/maximum value in a list and finding the associated month
def minmaxer(list, columnname):
    minimum = min(list)
    maximum = max(list)
    for row in data:
        if row[columnname] == str(minimum):
            minmonth = row["month"]
        elif row[columnname] == str(maximum):
            maxmonth = row["month"]
        else:
            continue
    return [minmonth, maxmonth]
minMaxSales = minmaxer(sales, "sales")
minMaxExpenditure = minmaxer(expenditure, "expenditure")
minMaxProfit = minmaxer(profit, "profit")

print(f"Total sales: {totalSale}\nTotal expenditure: {totalExpenditure}\nTotal profit: {totalProfit}\n")
print(f"Average monthly sale: {averageSale}\nAverage monthly expenditure: {averageExpenditure}\nAverage monthly profit: {averageProfit}\n")
print(f"Month with lowest sales:{minMaxSales[0]}\nMonth with highest sales:{minMaxSales[1]}\nMonth with lowest expenditure:{minMaxExpenditure[0]}\nMonth with highest expenditure:{minMaxExpenditure[1]}\nMonth with lowest profit:{minMaxProfit[0]}\nMonth with highest profit:{minMaxProfit[1]}\n")

file_path = 'sales.csv'
df = pd.read_csv(file_path)
df.columns = fieldnames

# Separating out monthly sales, expenditure and profit data for line graph 1
df1 = df.iloc[:, [1,2,3,4]]
df1.columns = ["month", "sales", "expenditure", "profit"]

# Separating out % change data for line graph 2
df2 = df.iloc[:, [1,5,6,7]]
df2.columns = ["month", "% change sales", "% change expenditure", "% change profit"]

sns.set_theme()
# Graph 1: Line graph of monthly sales, expenditure and profit
fig, ax = plt.subplots()
sns.lineplot(x = "month", y = "sales", data = df1, linewidth = 1, color = "orange", label = "Sales").set(title = "Cash flow 2018", xlabel = "Month", ylabel = "Monthly cash flow (GBP)")
sns.lineplot(x = "month", y = "expenditure", data = df1, linewidth = 1, color = "blue", label = "Expenditure")
sns.lineplot(x = "month", y = "profit", data = df1, linewidth = 1, color = "green", label = "Profit")
sns.lineplot(x = "month", y = averageSale, data = df1, linewidth = 1, linestyle = "dotted", color = "orange")
sns.lineplot(x = "month", y = averageExpenditure, data = df1, linewidth = 1, linestyle = "dotted", color = "blue")
sns.lineplot(x = "month", y = averageProfit, data = df1, linewidth = 1, linestyle = "dotted", color = "green")
plt.legend(loc= "lower right")

# Graph 2: Line graph of monthly percent change in sales, expenditure and profit
fig, ax1 = plt.subplots()
sns.lineplot(x = "month", y = "% change sales", data = df2, linewidth = 1, label = "% change sales").set(title = "Monthly percentage change 2018", xlabel = "Month", ylabel = "Change from previous month (%)")
sns.lineplot(x = "month", y = "% change expenditure", data = df2, linewidth = 1, label = "% change expenditure")
sns.lineplot(x = "month", y = "% change profit", data = df2, linewidth = 1, label = "% change profit")


# BAR GRAPH
# Extracting items from lists and putting them in a combined list called combinedCashFlow - used to make a list with all sales, expenditure and profit
combinedCashflow = []
def addToList(list):
    for item in list:
        combinedCashflow.append(item)
addToList(sales)
addToList(expenditure)
addToList(profit)
#print(combinedCashflow)

categoryList = []

# Making a list of labels for each category (12 each of sales, expenditure and profit)
def addCategory(categoryName):
    r = range(0,12)
    for n in r:
        categoryList.append(categoryName)
addCategory("Sales")
addCategory("Expenditure")
addCategory("Profit")

# Making dataframe of sales, expenditure and profit labeled with each category
cashFlowData = {"Yearly total (GBP)": combinedCashflow, "Category":categoryList}
df3 = pd.DataFrame(cashFlowData)
#print(cashFlowData)
print(df3)

fig, ax2 = plt.subplots()
sns.barplot(data = df3, x = "Category", y = "Yearly total (GBP)", width = 0.5, errorbar = "sd", capsize=0.1).set(title ="Summary for 2018", xlabel = "")

plt.show()
