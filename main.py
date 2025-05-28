import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

output_path = r"results"
base_path = "exam csv files"
items_df = pd.read_csv(f"{base_path}/Items.csv")
customers_df = pd.read_csv(f"{base_path}/customers.csv")
orders_df = pd.read_csv(f"{base_path}/orders.csv")
order_items_df = pd.read_csv(f"{base_path}/order_item.csv")
os.makedirs(output_path, exist_ok=True)

# הכנת נתונים

def select_best_item(group):
    return group.loc[group.notnull().sum(axis=1).idxmax()]

clean_items_df = items_df.groupby("item_name", group_keys=False).apply(select_best_item)
item_id_map = {}
for name, group in items_df.groupby("item_name"):
    if len(group) > 1:
        best = select_best_item(group)
        for _, row in group.iterrows():
            if row["id"] != best["id"]:
                item_id_map[row["id"]] = best["id"]
order_items_df["item_id"] = order_items_df["item_id"].replace(item_id_map)

def select_best_customer(group):
    return group.loc[group.notnull().sum(axis=1).idxmax()]

clean_customers_df = customers_df.groupby("email", group_keys=False).apply(select_best_customer)
customer_id_map = {}
for email, group in customers_df.groupby("email"):
    if len(group) > 1:
        best = select_best_customer(group)
        for _, row in group.iterrows():
            if row["id"] != best["id"]:
                customer_id_map[row["id"]] = best["id"]
orders_df["customer_id"] = orders_df["customer_id"].replace(customer_id_map)

def clean_missing(df, id_column):
    df = df.copy()
    for col in df.columns:
        if df[col].isna().sum() / len(df) > 0.05:
            if df[col].dtype == "object":
                df[col] = df[col].fillna("Unknown")
            else:
                df[col] = df[col].fillna(df[col].median())
        else:
            df = df[df[col].notna()]
    df = df[df[id_column].notna()]
    return df

clean_items_df = clean_missing(clean_items_df, "id")
clean_customers_df = clean_missing(clean_customers_df, "id")
orders_df = clean_missing(orders_df, "order_id")
order_items_df = clean_missing(order_items_df, "id")

# ניתוח לקוחות

gender_counts = clean_customers_df["gender"].value_counts()
age_distribution = clean_customers_df["age"].dropna()

clean_customers_df["joining_date"] = pd.to_datetime(clean_customers_df["joining_date"], errors="coerce")
clean_customers_df["year_joined"] = clean_customers_df["joining_date"].dt.year
yearly_joins = clean_customers_df["year_joined"].value_counts().sort_index()
clean_customers_df["month_joined"] = clean_customers_df["joining_date"].dt.month
monthly_joins = clean_customers_df.groupby("month_joined").size()

# ניתוח פריטים

category_counts = clean_items_df["item_category"].value_counts()
valid_stock_items = clean_items_df[clean_items_df["stock_quantity"] > 0]
max_stock = valid_stock_items.loc[valid_stock_items["stock_quantity"].idxmax()]
min_stock = valid_stock_items.loc[valid_stock_items["stock_quantity"].idxmin()]
mean_stock = valid_stock_items["stock_quantity"].mean()

# ניתוח הזמנות

order_counts = orders_df["customer_id"].value_counts()
orders_price_chart = order_counts.value_counts().sort_index()
top_customers = orders_df["customer_id"].value_counts().head(5).index
top_customers_df = clean_customers_df[clean_customers_df["id"].isin(top_customers)][["id", "first_name", "last_name"]]
payment_counts = orders_df["payment_method"].value_counts()

order_items_merged = pd.merge(order_items_df, clean_items_df[["id", "item_price"]], left_on="item_id", right_on="id", how="left")
order_items_merged["total_price"] = order_items_merged["quantity"] * order_items_merged["item_price"]
order_total_price = order_items_merged.groupby("order_id")["total_price"].sum().reset_index()
orders_df = pd.merge(orders_df, order_total_price, on="order_id", how="left")
orders_df["order_price_mean"] = np.mean(orders_df["total_price"] if "total_price" in orders_df else [0])
orders_df["order_price_std"] = np.std(orders_df["total_price"] if "total_price" in orders_df else [0])

order_stats = orders_df["total_price"].agg(["max", "min", "mean"])
mean_price = np.mean(orders_df["total_price"])
std_price = np.std(orders_df["total_price"])

order_items_count = order_items_df.groupby("order_id")["quantity"].sum().reset_index(name="total_items")
orders_scatter = pd.merge(orders_df, order_items_count, on="order_id")
scatter_data = orders_scatter[["delivery_days", "total_items"]].dropna()

ordered_customers = orders_df["customer_id"].unique()
no_order_customers = clean_customers_df[~clean_customers_df["id"].isin(ordered_customers)]

least_ordered_items = order_items_df.groupby("item_id")["quantity"].sum().nsmallest(5)


# גרפים:

sns.set(style="whitegrid")

plt.figure()
gender_counts.plot(kind="bar", title="Customers by Gender")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{output_path}/gender_distribution.png")

plt.figure()
age_distribution.plot(kind="hist", bins=20, title="Age Distribution")
plt.xlabel("Age")
plt.tight_layout()
plt.savefig(f"{output_path}/age_distribution.png")

plt.figure()
yearly_joins.plot(kind="bar", title="Yearly Customer Join Count")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{output_path}/yearly_joins.png")

plt.figure()
monthly_joins.plot(kind="bar", title="Monthly Customer Join Count")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig(f"{output_path}/monthly_joins.png")

plt.figure()
category_counts.plot(kind="pie", autopct='%1.1f%%', title="Items by Category")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{output_path}/item_category_pie.png")

plt.figure()
payment_counts.plot(kind="pie", autopct='%1.1f%%', title="Payment Methods")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{output_path}/payment_methods_pie.png")

plt.figure()
orders_price_chart.plot(kind="bar", title="Orders Per Customer")
plt.xlabel("Number of Orders")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(f"{output_path}/orders_histogram.png")

plt.figure()
plt.scatter(scatter_data["delivery_days"], scatter_data["total_items"])
plt.xlabel("Delivery Days")
plt.ylabel("Total Items in Order")
plt.title("Delivery Days vs Order Size")
plt.tight_layout()
plt.savefig(f"{output_path}/delivery_vs_items.png")

# פלטים לקבצים
#יש לך למטה אפשרות לחלץ עוד קובצים תרטה מה כתבתי שם
order_stats.to_csv(f"{output_path}/order_price_stats.csv")
no_order_customers.to_csv(f"{output_path}/customers_no_orders.csv", index=False)

print("less 5 Customers:")
print(least_ordered_items)
#least_ordered_items.to_csv(f"{output_path}/least_ordered_items.csv")
print("top 5 Customers:")
print(top_customers_df)
#אם אתה רוצה שזה יהיה גם בקובץ תשנה את זה גקי
#top_customers_df.to_csv(f"{output_path}/top_customers.csv", index=False)

# בונוס

orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
orders_august = orders_df[orders_df["order_date"].dt.month == 8]

usa_customers = clean_customers_df[clean_customers_df["nationallity"].str.lower() == "usa"]
usa_id = usa_customers["id"].values
usa_orders_aug = orders_august[orders_august["customer_id"].isin(usa_id)]

giftcard_orders_aug = orders_august[orders_august["payment_method"] == "GIFT_CARD"]
giftcard_total_aug = giftcard_orders_aug["total_price"].sum()
giftcard_total_other = orders_df[(orders_df["payment_method"] == "GIFT_CARD") & (orders_df["order_date"].dt.month != 8)]["total_price"].sum()


usa_giftcard_msg = np.where(
    giftcard_total_aug > giftcard_total_other,
    " there is an increase in gift card usage , the campaign might have worked!\n",
    " no significant change observed in gift card usage.\n"
)[()]

with open(f"{output_path}/summary.txt", "w", encoding="utf-8") as f:
    f.write(" exam Summary Conclusions:\n")
    f.write(f" number of orders in August from USA customers: {len(usa_orders_aug)} orders.\n")
    f.write(f" gift card usage in August: ${giftcard_total_aug:.2f}, compared to other months: ${giftcard_total_other:.2f}.\n")
    f.write(usa_giftcard_msg)

