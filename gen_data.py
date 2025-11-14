import csv, random
from datetime import datetime, timedelta

random.seed(42)

num_customers = 150
num_products = 120
num_orders = 200

first_names = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","William","Elizabeth","David","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Charles","Karen","Christopher","Nancy","Daniel","Lisa","Matthew","Betty","Anthony","Margaret","Mark","Sandra","Donald","Ashley","Steven","Kimberly","Paul","Emily","Andrew","Donna","Joshua","Michelle","Kenneth","Dorothy","Kevin","Carol","Brian","Amanda","George","Melissa","Edward","Deborah","Ronald","Stephanie","Timothy","Rebecca","Jason","Laura","Jeffrey","Sharon","Ryan","Cynthia","Jacob","Kathleen","Gary","Amy","Nicholas","Angela","Eric","Shirley","Jonathan","Anna","Larry","Brenda","Justin","Pamela","Scott","Emma","Brandon","Nicole","Benjamin","Helen","Samuel","Samantha","Frank","Katherine","Gregory","Christine","Raymond","Debra","Alexander","Rachel","Patrick","Carolyn","Jack","Janet","Dennis","Maria","Jerry","Heather","Tyler","Diane","Aaron","Julie","Jose","Joyce","Adam","Evelyn","Nathan","Frances","Henry","Joan","Zachary","Christina"]
last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts","Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes","Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper","Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson","Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes","Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez"]
cities = ["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","San Diego","Dallas","San Jose","Austin","Jacksonville","Fort Worth","Columbus","Charlotte","San Francisco","Indianapolis","Seattle","Denver","Washington","Boston","Nashville","El Paso","Detroit","Memphis","Portland","Oklahoma City","Las Vegas","Louisville","Baltimore","Milwaukee","Albuquerque","Tucson","Fresno","Sacramento","Mesa","Kansas City","Atlanta","Omaha","Colorado Springs","Raleigh","Miami","Virginia Beach","Oakland","Minneapolis","Tulsa","Arlington","New Orleans","Wichita"]
states = ["NY","CA","IL","TX","AZ","PA","OH","NC","WA","CO","FL","GA","NV","MA","TN","MI","MD","MO","OR","VA","MN","WI","LA","NM","KS","OK","KY","IN"]
streets = ["Main St","Oak Ave","Pine Rd","Maple Dr","Cedar Ln","Elm St","Walnut St","Sunset Blvd","Chestnut St","Hillcrest Rd","Riverside Ave","Highland Dr","Spruce St","Mulberry Ln","Park Ave","Broadway","River Rd","Forest Dr","Birch St","Sycamore Ln"]

categories = ["Electronics","Home","Beauty","Clothing","Sports","Toys","Books","Garden","Automotive","Health"]
product_names = {
    "Electronics": ["Wireless Earbuds","Smartphone","Bluetooth Speaker","Laptop","4K Monitor","Smartwatch","Gaming Console","Portable Charger","Wireless Mouse","Noise-Canceling Headphones"],
    "Home": ["Air Purifier","Vacuum Cleaner","Coffee Maker","Blender","Toaster Oven","Electric Kettle","Dish Set","Bed Sheets","Table Lamp","Scented Candle"],
    "Beauty": ["Moisturizing Cream","Face Serum","Shampoo","Conditioner","Hair Dryer","Perfume","Makeup Palette","Body Lotion","Facial Cleanser","Nail Polish Set"],
    "Clothing": ["Denim Jacket","Athletic Sneakers","Graphic T-Shirt","Chinos","Wool Sweater","Yoga Pants","Leather Belt","Baseball Cap","Winter Coat","Sundress"],
    "Sports": ["Running Shoes","Yoga Mat","Adjustable Dumbbells","Cycling Helmet","Tennis Racket","Basketball","Fitness Tracker","Hydration Backpack","Foam Roller","Resistance Bands"],
    "Toys": ["Building Blocks","Action Figure","Puzzle Set","Board Game","Stuffed Animal","Remote Control Car","Dollhouse","Art Kit","Science Kit","Rubik's Cube"],
    "Books": ["Mystery Novel","Cookbook","Self-Help Guide","Fantasy Epic","Historical Biography","Science Textbook","Travel Guide","Children's Storybook","Poetry Collection","Business Strategy Book"],
    "Garden": ["Planter Set","Garden Hose","Pruning Shears","Outdoor Chair","BBQ Grill","Herb Seeds","Solar Path Lights","Bird Feeder","Watering Can","Lawn Fertilizer"],
    "Automotive": ["Car Vacuum","Dash Cam","Seat Covers","Phone Mount","Tire Pressure Gauge","Jump Starter","Car Wax Kit","Floor Mats","Roof Rack","LED Headlights"],
    "Health": ["Vitamin Pack","Massage Gun","Electric Toothbrush","Water Flosser","Protein Powder","Yoga Block","Fitness Scale","First Aid Kit","Sleep Mask","Resistance Loop Set"]
}

countries = ["USA"]

start_date = datetime(2022,1,1)
end_date = datetime(2024,12,31)

def random_date():
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))

customers = []
for cid in range(1, num_customers+1):
    first = random.choice(first_names)
    last = random.choice(last_names)
    city = random.choice(cities)
    state = random.choice(states)
    addr = f"{random.randint(100, 9999)} {random.choice(streets)}"
    email = f"{first.lower()}.{last.lower()}{random.randint(1,99)}@example.com"
    phone = f"555-{random.randint(100,999)}-{random.randint(1000,9999)}"
    signup = random_date().date()
    customers.append([
        cid, first, last, email, phone, addr, city, state, random.choice(countries), signup.isoformat()
    ])

products = []
pid = 1
for category in categories:
    for name in product_names[category]:
        price = round(random.uniform(5, 500), 2)
        stock = random.randint(20, 1000)
        desc = f"{category} - {name}"
        products.append([pid, name, category, f"{price:.2f}", stock, desc])
        pid += 1
while len(products) < num_products:
    category = random.choice(categories)
    name = random.choice(product_names[category]) + f" {random.randint(2,9)}"
    price = round(random.uniform(5, 500), 2)
    stock = random.randint(20, 1000)
    desc = f"{category} - {name}"
    products.append([pid, name, category, f"{price:.2f}", stock, desc])
    pid += 1

orders = []
order_items = []
payments = []
order_id = 1
order_item_id = 1
payment_id = 1
status_options = ["Pending","Processing","Shipped","Delivered","Cancelled"]
payment_methods = ["Credit Card","PayPal","Bank Transfer","Gift Card","Apple Pay"]
payment_statuses = ["Completed","Pending","Failed"]
for _ in range(num_orders):
    customer = random.choice(customers)
    order_date = random_date()
    status = random.choices(status_options, weights=[0.15,0.2,0.25,0.3,0.1])[0]
    ship_addr = f"{customer[5]}, {customer[6]}, {customer[7]} {customer[8]}"
    num_items = random.randint(1,5)
    item_products = random.sample(products, num_items)
    total = 0
    for prod in item_products:
        qty = random.randint(1,4)
        price = float(prod[3])
        subtotal = round(qty*price,2)
        total = round(total + subtotal, 2)
        order_items.append([
            order_item_id,
            order_id,
            prod[0],
            qty,
            f"{price:.2f}",
            f"{subtotal:.2f}"
        ])
        order_item_id += 1
    total_str = f"{total:.2f}"
    orders.append([
        order_id,
        customer[0],
        order_date.date().isoformat(),
        status,
        ship_addr,
        total_str
    ])
    pay_status = "Completed" if status in ("Shipped","Delivered","Processing") else random.choice(payment_statuses)
    if status == "Cancelled":
        pay_status = random.choice(["Failed","Pending"])
        pay_amount = total if pay_status == "Completed" else 0
    else:
        pay_amount = total
    pay_date = (order_date + timedelta(days=random.randint(0,5))).date().isoformat()
    payments.append([
        payment_id,
        order_id,
        pay_date,
        f"{pay_amount:.2f}",
        random.choice(payment_methods),
        pay_status
    ])
    payment_id += 1
    order_id += 1

with open('Customers.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["CustomerID","FirstName","LastName","Email","Phone","Address","City","State","Country","SignupDate"])
    writer.writerows(customers)

with open('Products.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["ProductID","ProductName","Category","Price","StockQuantity","Description"])
    writer.writerows(products)

with open('Orders.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["OrderID","CustomerID","OrderDate","OrderStatus","ShippingAddress","TotalAmount"])
    writer.writerows(orders)

with open('OrderItems.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["OrderItemID","OrderID","ProductID","Quantity","UnitPrice","Subtotal"])
    writer.writerows(order_items)

with open('Payments.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["PaymentID","OrderID","PaymentDate","PaymentAmount","PaymentMethod","PaymentStatus"])
    writer.writerows(payments)

print("generated")
