import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

def generate_ecommerce_data(num_orders=10000):
    """
    Generates a realistic e-commerce transactions dataset (2024 - 2026).
    """
    print(f"Generating {num_orders} synthetic e-commerce transaction records...")

    # Customer base setup (1,200 unique customers)
    num_customers = 1200
    customer_ids = [f"CUST-{1000 + i}" for i in range(num_customers)]

    # Demographics / Attributes
    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    region_weights = [0.40, 0.30, 0.20, 0.10]
    customer_region_map = {c_id: np.random.choice(regions, p=region_weights) for c_id in customer_ids}

    # Product catalog setup
    products_catalog = [
        {"product_id": "PROD-101", "name": "Wireless Noise-Canceling Headphones", "category": "Electronics", "unit_price": 199.99},
        {"product_id": "PROD-102", "name": "Ultra-Wide Gaming Monitor 34\"", "category": "Electronics", "unit_price": 499.50},
        {"product_id": "PROD-103", "name": "Smart Fitness Watch V2", "category": "Electronics", "unit_price": 149.00},
        {"product_id": "PROD-104", "name": "Mechanical Ergonomic Keyboard", "category": "Electronics", "unit_price": 119.99},
        {"product_id": "PROD-201", "name": "Organic Cotton Oversized Hoodie", "category": "Apparel", "unit_price": 65.00},
        {"product_id": "PROD-202", "name": "Premium Denim Jacket", "category": "Apparel", "unit_price": 89.95},
        {"product_id": "PROD-203", "name": "Performance Running Shoes", "category": "Apparel", "unit_price": 120.00},
        {"product_id": "PROD-301", "name": "Ergonomic Memory Foam Chair", "category": "Home & Living", "unit_price": 249.99},
        {"product_id": "PROD-302", "name": "Smart Ambient Desk Lamp", "category": "Home & Living", "unit_price": 45.50},
        {"product_id": "PROD-303", "name": "Automatic Espresso Coffee Maker", "category": "Home & Living", "unit_price": 299.00},
        {"product_id": "PROD-401", "name": "Hydrating Facial Serum Set", "category": "Beauty & Health", "unit_price": 38.00},
        {"product_id": "PROD-402", "name": "Sonic Electric Toothbrush", "category": "Beauty & Health", "unit_price": 54.99},
        {"product_id": "PROD-501", "name": "Data Analytics & ML Handbook", "category": "Books", "unit_price": 42.50},
        {"product_id": "PROD-502", "name": "Executive Leadership & Strategy", "category": "Books", "unit_price": 28.99},
    ]

    # Time frame: Jan 1, 2024 to Sep 20, 2026
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 9, 20)
    total_days = (end_date - start_date).days

    # Payment methods and probabilities
    payment_methods = ["Credit Card", "PayPal", "Apple Pay", "Debit Card", "UPI / NetBanking"]
    payment_weights = [0.45, 0.25, 0.15, 0.10, 0.05]

    orders = []

    # Assign customer signup cohorts (first purchase date)
    customer_signup_date = {}
    for c_id in customer_ids:
        # Uniform spread of signup dates over the timeframe
        days_offset = np.random.randint(0, total_days - 30)
        customer_signup_date[c_id] = start_date + timedelta(days=days_offset)

    for i in range(1, num_orders + 1):
        order_id = f"ORD-{2024000 + i}"
        
        # Pick customer (favoring active customers to simulate repurchase frequency)
        c_id = np.random.choice(customer_ids)
        c_signup = customer_signup_date[c_id]
        
        # Order date must be >= customer signup date
        max_possible_offset = (end_date - c_signup).days
        if max_possible_offset <= 0:
            order_days_offset = 0
        else:
            # Non-linear probability to simulate retention decay
            order_days_offset = int(np.random.exponential(scale=180))
            order_days_offset = min(order_days_offset, max_possible_offset)
            
        order_date = c_signup + timedelta(days=order_days_offset)

        # Select product
        prod = np.random.choice(products_catalog)

        # Quantity (mostly 1 to 3)
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.60, 0.25, 0.10, 0.03, 0.02])

        # Unit Price with slight fluctuation/discounts
        base_unit_price = prod["unit_price"]
        
        # Discount percent (0%, 5%, 10%, 15%, 20%) - Higher in Nov/Dec
        if order_date.month in [11, 12]:
            discount_pct = np.random.choice([0.10, 0.15, 0.20, 0.25], p=[0.2, 0.3, 0.3, 0.2])
        else:
            discount_pct = np.random.choice([0.0, 0.05, 0.10, 0.15], p=[0.5, 0.3, 0.15, 0.05])

        discount_amount = round(base_unit_price * quantity * discount_pct, 2)
        gross_amount = round(base_unit_price * quantity, 2)
        net_amount = round(gross_amount - discount_amount, 2)

        # Shipping cost
        shipping_cost = 0.0 if net_amount > 100 else 9.99

        # Payment method & Order status
        payment = np.random.choice(payment_methods, p=payment_weights)
        status = np.random.choice(["Completed", "Returned", "Cancelled"], p=[0.88, 0.08, 0.04])

        region = customer_region_map[c_id]

        orders.append({
            "order_id": order_id,
            "order_date": order_date.strftime("%Y-%m-%d %H:%M:%S"),
            "customer_id": c_id,
            "region": region,
            "product_id": prod["product_id"],
            "product_name": prod["name"],
            "category": prod["category"],
            "quantity": quantity,
            "unit_price": base_unit_price,
            "gross_amount": gross_amount,
            "discount_pct": round(discount_pct * 100, 1),
            "discount_amount": discount_amount,
            "net_amount": net_amount,
            "shipping_cost": shipping_cost,
            "total_revenue": round(net_amount + shipping_cost, 2),
            "payment_method": payment,
            "order_status": status
        })

    df = pd.DataFrame(orders)
    
    # Introduce ~0.5% missing values in payment_method or region to demonstrate data cleaning skills
    missing_indices = np.random.choice(df.index, size=int(len(df) * 0.005), replace=False)
    df.loc[missing_indices, "payment_method"] = np.nan

    os.makedirs("data", exist_ok=True)
    raw_path = os.path.join("data", "raw_ecommerce_data.csv")
    df.to_csv(raw_path, index=False)
    print(f"Dataset saved successfully to '{raw_path}' with shape {df.shape}")
    return df

if __name__ == "__main__":
    generate_ecommerce_data(10000)
