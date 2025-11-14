import csv, random
from datetime import datetime, timedelta

random.seed(42)

first_names = ["Emma","Liam","Olivia","Noah","Ava","Ethan","Sophia","Mason","Isabella","Logan","Mia","Lucas","Charlotte","Jackson","Amelia","Aiden","Harper","Elijah","Evelyn","Oliver","Abigail","Jacob","Emily","Michael","Elizabeth","Daniel","Sofia","Henry","Avery","Sebastian","Ella","Jack","Scarlett","Alexander","Grace","Carter","Chloe","Wyatt","Victoria","Jayden","Riley","Leo","Aria","Gabriel","Lily","Anthony","Penelope","Isaac","Layla","Grayson","Nora","Hudson","Zoey","Matthew","Mila","Ezra","Hannah","Lincoln","Lillian","Luke","Addison","Julian","Eleanor","Owen","Natalie","Caleb","Luna","Ryan","Savannah","Nathan","Brooklyn","Thomas","Leah","Charles","Zoe","Christopher","Stella","Jaxon","Hazel","Miles","Ellie","Isaiah","Paisley","Andrew","Audrey","Joshua","Skylar","Jose","Violet","Christian","Claire","Hunter","Bella","Eli","Aurora","Jonathan","Lucy","Connor","Anna"]
last_names = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts","Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes","Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper","Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson","Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes","Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross"]
streets = ["Maple St","Oak Ave","Pine Rd","Cedar Ln","Elm St","Walnut Dr","Birch Ct","Chestnut Blvd","Willow Way","Aspen Cir","Highland Rd","River St","Sunset Ave","Forest Dr","Lakeside Blvd","Hillcrest Rd","Sycamore St","Meadow Ln","Park Ave","Spruce St"]
cities = ["Seattle","Austin","Denver","Boston","Chicago","Phoenix","San Diego","Portland","Atlanta","Dallas","San Jose","Miami","Orlando","Nashville","Charlotte","Columbus","Indianapolis","Detroit","Minneapolis","Tampa","Raleigh","Baltimore","Cincinnati","Cleveland","Pittsburgh","Kansas City","Salt Lake City","Las Vegas","Richmond","St. Louis","Milwaukee","New Orleans","Memphis","Hartford","Providence","Albany","Sacramento","San Antonio","Boulder","Madison"]
states = ["WA","TX","CO","MA","IL","AZ","CA","OR","GA","NC","FL","OH","MI","MN","UT","NV","VA","MO","WI","LA","TN","CT","RI","NY","PA","MD"]

customer_rows = []
base_date = datetime(2020,1,1)
for cid in range(1,101):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    email = f"{fn.lower()}.{ln.lower()}{cid}@example.com"
    phone = f"555-{random.randint(1000000,9999999)}"
    addr = f"{random.randint(100,999)} {random.choice(streets)}"
    city = random.choice(cities)
    state = random.choice(states)
    signup = base_date + timedelta(days=random.randint(0,1825))
    customer_rows.append([cid,fn,ln,email,phone,addr,city,state,"USA",signup.strftime("%Y-%m-%d")])

categories = ["Electronics","Home","Fashion","Sports","Beauty","Toys","Books","Garden","Automotive","Office"]
product_rows = []
for pid in range(1,101):
    cat = random.choice(categories)
    pname = f"{cat} Item {pid}"
    price = round(random.uniform(5,500),2)
    stock = random.randint(10,500)
    desc = f"High-quality {cat.lower()} product #{pid}"
    product_rows.append([pid,pname,cat,f"{price:.2f}",stock,desc])

order_statuses = ["Pending","Processing","Shipped","Delivered","Cancelled"]
num_orders = 120
order_rows = []
order_totals = {}
for oid in range(1,num_orders+1):
    cust_id = random.randint(1,100)
    odate = base_date + timedelta(days=random.randint(0,1825))
    status = random.choices(order_statuses,weights=[10,20,30,35,5])[0]
    customer = customer_rows[cust_id-1]
    ship_addr = f"{customer[5]}, {customer[6]}, {customer[7]}"
    order_rows.append([oid,cust_id,odate.strftime("%Y-%m-%d"),status,ship_addr,0])
    order_totals[oid] = 0

order_item_rows = []
order_item_id = 1
for oid in range(1,num_orders+1):
    num_items = random.randint(1,4)
    products = random.sample(product_rows,k=num_items)
    subtotal_sum = 0
    for prod in products:
        qty = random.randint(1,5)
        price = float(prod[3])
        subtotal = round(qty*price,2)
        subtotal_sum += subtotal
        order_item_rows.append([order_item_id,oid,prod[0],qty,f"{price:.2f}",f"{subtotal:.2f}"])
        order_item_id+=1
    order_totals[oid]+=round(subtotal_sum,2)

for row in order_rows:
    row[5] = f"{order_totals[row[0]]:.2f}"

payment_methods = ["Credit Card","PayPal","Gift Card","Bank Transfer","Apple Pay"]
payment_statuses = ["Completed","Pending","Failed","Refunded"]
payment_rows = []
payment_id = 1
for oid in range(1,num_orders+1):
    pay_date = base_date + timedelta(days=random.randint(0,1825))
    amount = order_totals[oid]
    method = random.choice(payment_methods)
    status = random.choices(payment_statuses,weights=[70,15,10,5])[0]
    payment_rows.append([payment_id,oid,pay_date.strftime("%Y-%m-%d"),f"{amount:.2f}",method,status])
    payment_id +=1

files = [
    ("Customers.csv", ["CustomerID","FirstName","LastName","Email","Phone","Address","City","State","Country","SignupDate"], customer_rows),
    ("Products.csv", ["ProductID","ProductName","Category","Price","StockQuantity","Description"], product_rows),
    ("Orders.csv", ["OrderID","CustomerID","OrderDate","OrderStatus","ShippingAddress","TotalAmount"], order_rows),
    ("OrderItems.csv", ["OrderItemID","OrderID","ProductID","Quantity","UnitPrice","Subtotal"], order_item_rows),
    ("Payments.csv", ["PaymentID","OrderID","PaymentDate","PaymentAmount","PaymentMethod","PaymentStatus"], payment_rows),
]

for fname, header, rows in files:
    with open(fname,'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

print("done")
