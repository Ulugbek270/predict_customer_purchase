import asyncio
from datetime import datetime, timedelta
import random
from sqlalchemy.ext.asyncio import AsyncSession
from models.tables.tables_all import Goods, ClientLocal, Agent, Requirement, RequirementGoods
from core.conn import connection


async def generate_mock_data(session: AsyncSession):
    """Generate comprehensive mock data for the database"""

    # 1. Create Goods (Products) - 50 items
    goods_data = [
        # Grains & Flour
        {"name_en": "Wheat Flour Premium"},
        {"name_en": "Wheat Flour Standard"},
        {"name_en": "Rice Basmati"},
        {"name_en": "Rice Jasmine"},
        {"name_en": "Rice Long Grain"},
        {"name_en": "Buckwheat"},
        {"name_en": "Oatmeal"},
        {"name_en": "Cornmeal"},
        {"name_en": "Semolina"},
        {"name_en": "Pearl Barley"},

        # Oils & Fats
        {"name_en": "Sunflower Oil 1L"},
        {"name_en": "Sunflower Oil 5L"},
        {"name_en": "Olive Oil"},
        {"name_en": "Vegetable Oil"},
        {"name_en": "Butter"},
        {"name_en": "Margarine"},

        # Sugar & Sweeteners
        {"name_en": "White Sugar"},
        {"name_en": "Brown Sugar"},
        {"name_en": "Honey Natural"},
        {"name_en": "Honey Acacia"},

        # Pasta & Noodles
        {"name_en": "Pasta Spaghetti"},
        {"name_en": "Pasta Penne"},
        {"name_en": "Pasta Fusilli"},
        {"name_en": "Instant Noodles"},
        {"name_en": "Vermicelli"},

        # Canned Goods
        {"name_en": "Tomato Paste"},
        {"name_en": "Canned Beans"},
        {"name_en": "Canned Corn"},
        {"name_en": "Canned Peas"},
        {"name_en": "Canned Tomatoes"},
        {"name_en": "Canned Fish Tuna"},
        {"name_en": "Canned Fish Sardines"},

        # Beverages
        {"name_en": "Black Tea Premium"},
        {"name_en": "Black Tea Standard"},
        {"name_en": "Green Tea"},
        {"name_en": "Instant Coffee"},
        {"name_en": "Ground Coffee"},
        {"name_en": "Cocoa Powder"},

        # Dairy Products
        {"name_en": "Milk Powder"},
        {"name_en": "Condensed Milk"},
        {"name_en": "Cream Powder"},

        # Spices & Seasonings
        {"name_en": "Salt Iodized"},
        {"name_en": "Black Pepper"},
        {"name_en": "Red Pepper"},
        {"name_en": "Cumin"},
        {"name_en": "Cinnamon"},
        {"name_en": "Bay Leaf"},

        # Miscellaneous
        {"name_en": "Yeast Dry"},
        {"name_en": "Baking Powder"},
        {"name_en": "Vinegar"},
    ]

    goods_list = []
    for item in goods_data:
        goods = Goods(**item)
        session.add(goods)
        goods_list.append(goods)

    await session.flush()
    print(f"✅ Created {len(goods_list)} goods")

    # 2. Create Local Clients - 30 clients
    clients_data = [
        {"name_ru": "ООО Продукты Плюс", "contact_name": "Иванов Иван Иванович", "phone": "+998901234567",
         "email": "ivanov@produkty.uz"},
        {"name_ru": "ТОО Торговый Дом", "contact_name": "Петрова Мария Сергеевна", "phone": "+998901234568",
         "email": "petrova@td.uz"},
        {"name_ru": "ИП Абдуллаев", "contact_name": "Абдуллаев Рашид", "phone": "+998901234569",
         "email": "abdullaev@mail.uz"},
        {"name_ru": "Супермаркет Олтин", "contact_name": "Каримов Азиз", "phone": "+998901234570",
         "email": "karimov@oltin.uz"},
        {"name_ru": "Магазин У Дома", "contact_name": "Сидорова Анна", "phone": "+998901234571",
         "email": "sidorova@udoma.uz"},
        {"name_ru": "Оптторг Навои", "contact_name": "Алимов Шерзод", "phone": "+998901234572",
         "email": "alimov@navoi.uz"},
        {"name_ru": "ООО Гастроном", "contact_name": "Смирнов Петр", "phone": "+998901234573",
         "email": "smirnov@gastro.uz"},
        {"name_ru": "Мини-маркет Дустлик", "contact_name": "Юсупова Нигора", "phone": "+998901234574",
         "email": "yusupova@dustlik.uz"},
        {"name_ru": "ТД Восток", "contact_name": "Рахимов Фарход", "phone": "+998901234575",
         "email": "rahimov@vostok.uz"},
        {"name_ru": "ИП Хасанов", "contact_name": "Хасанов Тимур", "phone": "+998901234576",
         "email": "hasanov@trade.uz"},
        {"name_ru": "Супермаркет Азия", "contact_name": "Ким Сергей", "phone": "+998901234577", "email": "kim@asia.uz"},
        {"name_ru": "ООО Продснаб", "contact_name": "Кузнецова Елена", "phone": "+998901234578",
         "email": "kuznetsova@prodsnab.uz"},
        {"name_ru": "Магазин Бахор", "contact_name": "Джалилов Жасур", "phone": "+998901234579",
         "email": "jalilov@bahor.uz"},
        {"name_ru": "ТД Самарканд", "contact_name": "Мирзаева Гульнора", "phone": "+998901234580",
         "email": "mirzaeva@samarkand.uz"},
        {"name_ru": "ИП Назаров", "contact_name": "Назаров Бахтиёр", "phone": "+998901234581",
         "email": "nazarov@biz.uz"},
        {"name_ru": "Гипермаркет Макро", "contact_name": "Волков Дмитрий", "phone": "+998901234582",
         "email": "volkov@makro.uz"},
        {"name_ru": "ООО Универсам", "contact_name": "Камилова Севара", "phone": "+998901234583",
         "email": "kamilova@universam.uz"},
        {"name_ru": "Магазин Нур", "contact_name": "Усманов Одил", "phone": "+998901234584", "email": "usmanov@nur.uz"},
        {"name_ru": "ТД Фергана", "contact_name": "Соколова Ольга", "phone": "+998901234585",
         "email": "sokolova@fergana.uz"},
        {"name_ru": "ИП Ахмедов", "contact_name": "Ахмедов Алишер", "phone": "+998901234586",
         "email": "ahmedov@trade.uz"},
        {"name_ru": "Супермаркет Звезда", "contact_name": "Морозов Андрей", "phone": "+998901234587",
         "email": "morozov@zvezda.uz"},
        {"name_ru": "ООО Оптима", "contact_name": "Садыкова Дильбар", "phone": "+998901234588",
         "email": "sadykova@optima.uz"},
        {"name_ru": "Магазин Шодлик", "contact_name": "Исмаилов Шохрух", "phone": "+998901234589",
         "email": "ismailov@shodlik.uz"},
        {"name_ru": "ТД Андижан", "contact_name": "Новикова Ирина", "phone": "+998901234590",
         "email": "novikova@andijan.uz"},
        {"name_ru": "ИП Мамедов", "contact_name": "Мамедов Эльдар", "phone": "+998901234591",
         "email": "mamedov@shop.uz"},
        {"name_ru": "Гипермаркет Центр", "contact_name": "Павлов Игорь", "phone": "+998901234592",
         "email": "pavlov@centr.uz"},
        {"name_ru": "ООО Меркурий", "contact_name": "Холматова Малика", "phone": "+998901234593",
         "email": "holmatova@mercury.uz"},
        {"name_ru": "Магазин Файзли", "contact_name": "Файзуллаев Санжар", "phone": "+998901234594",
         "email": "fayzullaev@shop.uz"},
        {"name_ru": "ТД Бухара", "contact_name": "Егорова Татьяна", "phone": "+998901234595",
         "email": "egorova@buhara.uz"},
        {"name_ru": "ИП Турсунов", "contact_name": "Турсунов Давлат", "phone": "+998901234596",
         "email": "tursunov@trade.uz"},
    ]

    clients_list = []
    for client_data in clients_data:
        client = ClientLocal(**client_data)
        session.add(client)
        clients_list.append(client)

    await session.flush()
    print(f"✅ Created {len(clients_list)} clients")

    # 3. Create Agents (Independent sellers) - 15 agents
    agents_data = [
        {"full_name": "Хасанов Тимур Рашидович", "phone": "+998912345671", "email": "hasanov@agent.uz"},
        {"full_name": "Рахимова Нигора Азизовна", "phone": "+998912345672", "email": "rahimova@agent.uz"},
        {"full_name": "Усманов Фарход Шерзодович", "phone": "+998912345673", "email": "usmanov@agent.uz"},
        {"full_name": "Юсупова Дилноза Камиловна", "phone": "+998912345674", "email": "yusupova@agent.uz"},
        {"full_name": "Назаров Бахтиёр Одилович", "phone": "+998912345675", "email": "nazarov@agent.uz"},
        {"full_name": "Камилова Севара Алишеровна", "phone": "+998912345676", "email": "kamilova@agent.uz"},
        {"full_name": "Джалилов Жасур Файзуллаевич", "phone": "+998912345677", "email": "jalilov@agent.uz"},
        {"full_name": "Мирзаева Гульнора Давлатовна", "phone": "+998912345678", "email": "mirzaeva@agent.uz"},
        {"full_name": "Алимов Шохрух Санжарович", "phone": "+998912345679", "email": "alimov@agent.uz"},
        {"full_name": "Холматова Малика Эльдаровна", "phone": "+998912345680", "email": "holmatova@agent.uz"},
        {"full_name": "Исмаилов Одил Игоревич", "phone": "+998912345681", "email": "ismailov@agent.uz"},
        {"full_name": "Садыкова Дильбар Андреевна", "phone": "+998912345682", "email": "sadykova@agent.uz"},
        {"full_name": "Файзуллаев Алишер Петрович", "phone": "+998912345683", "email": "fayzullaev@agent.uz"},
        {"full_name": "Турсунов Шерзод Дмитриевич", "phone": "+998912345684", "email": "tursunov@agent.uz"},
        {"full_name": "Ахмедов Давлат Сергеевич", "phone": "+998912345685", "email": "ahmedov@agent.uz"},
    ]

    agents_list = []
    for agent_data in agents_data:
        agent = Agent(**agent_data)
        session.add(agent)
        agents_list.append(agent)

    await session.flush()
    print(f"✅ Created {len(agents_list)} agents")

    # 4. Create Requirements with realistic patterns
    # Generate requirements over the past 12 months
    start_date = datetime.now() - timedelta(days=365)
    total_requirements = 0
    total_items = 0

    for client in clients_list:
        # Each client orders 3-8 different products regularly
        num_products = random.randint(3, 8)
        client_products = random.sample(goods_list, num_products)

        # Generate 8-20 requirements over 12 months (more data!)
        num_requirements = random.randint(8, 20)

        # Create somewhat regular ordering patterns
        # Some clients order weekly, some bi-weekly, some monthly
        order_frequency = random.choice([7, 14, 21, 30])  # days between orders

        for req_num in range(num_requirements):
            # Create somewhat regular intervals with some randomness
            base_days = req_num * order_frequency
            days_offset = base_days + random.randint(-3, 3)
            days_offset = min(days_offset, 365)
            req_date = start_date + timedelta(days=days_offset)

            # Pick a random agent (agents work with multiple clients)
            agent = random.choice(agents_list)

            # Create requirement
            requirement = Requirement(
                agent_id=agent.id,
                client_local_id=client.id,
                date=req_date
            )
            session.add(requirement)
            await session.flush()
            total_requirements += 1

            # Add 2-6 items to this requirement
            num_items = random.randint(2, 6)
            requirement_products = random.sample(client_products, min(num_items, len(client_products)))

            for goods in requirement_products:
                # Generate realistic amounts based on product type
                if "Oil" in goods.name_en or "Flour" in goods.name_en:
                    base_amount = random.choice([50, 100, 200, 500, 1000])
                elif "Sugar" in goods.name_en or "Rice" in goods.name_en:
                    base_amount = random.choice([20, 50, 100, 200, 500])
                elif "Tea" in goods.name_en or "Coffee" in goods.name_en:
                    base_amount = random.choice([10, 20, 50, 100])
                elif "Pasta" in goods.name_en or "Noodles" in goods.name_en:
                    base_amount = random.choice([30, 50, 100, 200])
                else:
                    base_amount = random.choice([10, 20, 50, 100, 200])

                # Add variation to amounts (±20%)
                amount = base_amount * random.uniform(0.8, 1.2)

                # Generate prices with slight variations over time
                # Simulate price inflation over the year
                time_factor = days_offset / 365.0
                inflation_factor = 1 + (time_factor * 0.1)  # 10% inflation over the year

                if "Premium" in goods.name_en:
                    base_price = random.uniform(50, 200)
                elif "Oil" in goods.name_en:
                    base_price = random.uniform(30, 80)
                elif "Flour" in goods.name_en or "Rice" in goods.name_en:
                    base_price = random.uniform(20, 60)
                elif "Tea" in goods.name_en or "Coffee" in goods.name_en:
                    base_price = random.uniform(40, 150)
                else:
                    base_price = random.uniform(10, 100)

                cost_sell = round(base_price * inflation_factor * random.uniform(0.95, 1.05), 2)

                item = RequirementGoods(
                    requirement_id=requirement.id,
                    goods_id=goods.id,
                    amount=round(amount, 2),
                    cost_sell=cost_sell
                )
                session.add(item)
                total_items += 1

    await session.commit()
    print("\n" + "=" * 60)
    print("🎉 MOCK DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"📦 Goods created:        {len(goods_list)}")
    print(f"🏢 Clients created:      {len(clients_list)}")
    print(f"👤 Agents created:       {len(agents_list)}")
    print(f"📋 Requirements created: {total_requirements}")
    print(f"📊 Items created:        {total_items}")
    print(f"📈 Avg items per req:    {total_items / total_requirements:.1f}")
    print("=" * 60)


@connection
async def run_mock_data_generation(session: AsyncSession):
    """Wrapper function to use with @connection decorator"""
    await generate_mock_data(session)


# Run this to populate the database
if __name__ == "__main__":
    asyncio.run(run_mock_data_generation())