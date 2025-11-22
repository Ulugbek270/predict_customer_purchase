import asyncio
import random
from datetime import datetime, timedelta

from core.base import async_session
from models.tables.clients import Client
from models.tables.customers import Customer
from models.tables.goods import Goods
from models.tables.orders import Order
from models.tables.order_items import OrderItem

# Sample data
client_names = [f"Company {i}" for i in range(1, 21)]
contact_names = [f"Contact {i}" for i in range(1, 21)]
customer_names = [f"Customer {i}" for i in range(1, 41)]
goods_names = ["Sand", "Cement", "Bricks", "Steel Rods", "Paint", "Tiles",
               "Wood Planks", "Gravel", "Concrete Mix", "Insulation",
               "Pipes", "Electrical Wire", "Plywood", "Nails", "Screws"]
units = ["ton", "bag", "pcs", "m³", "liter", "kg", "meter"]


async def create_realistic_orders(session, clients, goods_list):
    """
    Create realistic orders with patterns for prediction testing
    """
    orders = []

    # Define purchase patterns for different client-product combinations
    patterns = [
        # Regular patterns (high confidence)
        {"client_idx": 0, "goods_idx": 0, "cycle_days": 30, "variance": 2, "quantity": 5},
        # Company 1 buys Sand every 30 days
        {"client_idx": 0, "goods_idx": 1, "cycle_days": 45, "variance": 3, "quantity": 10},
        # Company 1 buys Cement every 45 days
        {"client_idx": 1, "goods_idx": 2, "cycle_days": 14, "variance": 1, "quantity": 100},
        # Company 2 buys Bricks every 14 days
        {"client_idx": 1, "goods_idx": 3, "cycle_days": 60, "variance": 5, "quantity": 20},
        # Company 2 buys Steel every 60 days
        {"client_idx": 2, "goods_idx": 0, "cycle_days": 28, "variance": 3, "quantity": 3},
        # Company 3 buys Sand every 28 days
        {"client_idx": 2, "goods_idx": 4, "cycle_days": 90, "variance": 7, "quantity": 50},
        # Company 3 buys Paint every 90 days
        {"client_idx": 3, "goods_idx": 1, "cycle_days": 21, "variance": 2, "quantity": 15},
        # Company 4 buys Cement every 21 days
        {"client_idx": 4, "goods_idx": 5, "cycle_days": 35, "variance": 4, "quantity": 200},
        # Company 5 buys Tiles every 35 days

        # Medium regularity patterns (medium confidence)
        {"client_idx": 5, "goods_idx": 6, "cycle_days": 40, "variance": 8, "quantity": 30},
        {"client_idx": 6, "goods_idx": 7, "cycle_days": 50, "variance": 10, "quantity": 8},

        # Irregular patterns (low confidence)
        {"client_idx": 7, "goods_idx": 8, "cycle_days": 45, "variance": 20, "quantity": 25},
        {"client_idx": 8, "goods_idx": 9, "cycle_days": 60, "variance": 25, "quantity": 40},
    ]

    # Generate orders based on patterns
    for pattern in patterns:
        client = clients[pattern["client_idx"]]
        goods = goods_list[pattern["goods_idx"]]

        # Generate 5-8 orders per pattern (enough for prediction)
        num_orders = random.randint(5, 8)
        current_date = datetime.now() - timedelta(days=pattern["cycle_days"] * num_orders + 10)  # Add +10 buffer

        for i in range(num_orders):
            # Add variance to cycle
            cycle_variation = random.randint(-pattern["variance"], pattern["variance"])
            current_date += timedelta(days=pattern["cycle_days"] + cycle_variation)

            # Create order
            quantity = pattern["quantity"] + random.randint(-2, 2)
            total_amount = goods.price * quantity

            order = Order(
                client_id=client.id,
                order_date=current_date,
                total_amount=total_amount
            )
            session.add(order)
            await session.flush()  # Get order.id

            # Create order item
            item = OrderItem(
                order_id=order.id,
                goods_id=goods.id,
                quantity=quantity,
                price_at_time=goods.price
            )
            session.add(item)
            orders.append(order)

    # Add some random orders for other clients (noise data)
    for _ in range(20):
        client = random.choice(clients[9:])  # Use clients without patterns
        goods = random.choice(goods_list)
        order_date = datetime.now() - timedelta(days=random.randint(0, 180))
        quantity = random.randint(1, 10)
        total_amount = goods.price * quantity

        order = Order(
            client_id=client.id,
            order_date=order_date,
            total_amount=total_amount
        )
        session.add(order)
        await session.flush()

        item = OrderItem(
            order_id=order.id,
            goods_id=goods.id,
            quantity=quantity,
            price_at_time=goods.price
        )
        session.add(item)
        orders.append(order)

    return orders


async def populate_db():
    async with async_session() as session:
        # 1️⃣ Clients
        print("Creating clients...")
        clients = []
        for i in range(20):
            client = Client(
                name=client_names[i],
                contact_name=random.choice(contact_names),
                phone=f"+998{random.randint(901000000, 999999999)}",
                email=f"client{i}@example.com"
            )
            session.add(client)
            clients.append(client)
        await session.commit()
        print(f"✅ Created {len(clients)} clients")

        # 2️⃣ Customers
        print("Creating customers...")
        customers = []
        for i in range(40):
            customer = Customer(
                client_id=random.choice(clients).id,
                full_name=random.choice(customer_names),
                phone=f"+998{random.randint(901000000, 999999999)}",
                email=f"customer{i}@example.com"
            )
            session.add(customer)
            customers.append(customer)
        await session.commit()
        print(f"✅ Created {len(customers)} customers")

        # 3️⃣ Goods
        print("Creating goods...")
        goods_list = []
        for i in range(len(goods_names)):
            goods = Goods(
                name=goods_names[i],
                unit=units[i % len(units)],
                price=round(random.uniform(10, 500), 2),
                is_active=True
            )
            session.add(goods)
            goods_list.append(goods)
        await session.commit()
        print(f"✅ Created {len(goods_list)} goods")

        # 4️⃣ Orders with realistic patterns
        print("Creating orders with purchase patterns...")
        orders = await create_realistic_orders(session, clients, goods_list)
        await session.commit()
        print(f"✅ Created {len(orders)} orders with realistic patterns")

        print("\n" + "=" * 60)
        print("✅ DB populated with realistic mock data for predictions!")
        print("=" * 60)
        print("\n📊 Pattern Summary:")
        print("- Company 1: Buys Sand every ~30 days, Cement every ~45 days")
        print("- Company 2: Buys Bricks every ~14 days, Steel every ~60 days")
        print("- Company 3: Buys Sand every ~28 days, Paint every ~90 days")
        print("- Company 4: Buys Cement every ~21 days")
        print("- Company 5: Buys Tiles every ~35 days")
        print("- + 7 more patterns with varying regularity")
        print("- + 20 random orders for noise\n")


if __name__ == "__main__":
    asyncio.run(populate_db())