$rand = [System.Random]::new(314)

function Get-RandomFrom {
    param([object[]]$Array)
    return $Array[$rand.Next(0, $Array.Count)]
}

function Get-RandomDate {
    $start = Get-Date -Date '2022-01-01'
    $end = Get-Date -Date '2024-12-31'
    $range = ($end - $start).Days
    return $start.AddDays($rand.Next(0, $range + 1))
}

function Get-RandomSample {
    param([System.Collections.IList]$List, [int]$Count)
    if ($Count -ge $List.Count) { return $List }
    $indices = [System.Collections.Generic.HashSet[int]]::new()
    while ($indices.Count -lt $Count) {
        [void]$indices.Add($rand.Next(0, $List.Count))
    }
    return $indices | ForEach-Object { $List[$_] }
}

$firstNames = @("James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","William","Elizabeth","David","Barbara","Richard","Susan","Joseph","Jessica","Thomas","Sarah","Charles","Karen","Christopher","Nancy","Daniel","Lisa","Matthew","Betty","Anthony","Margaret","Mark","Sandra","Donald","Ashley","Steven","Kimberly","Paul","Emily","Andrew","Donna","Joshua","Michelle","Kenneth","Dorothy","Kevin","Carol","Brian","Amanda","George","Melissa","Edward","Deborah","Ronald","Stephanie","Timothy","Rebecca","Jason","Laura","Jeffrey","Sharon","Ryan","Cynthia","Jacob","Kathleen","Gary","Amy","Nicholas","Angela","Eric","Shirley","Jonathan","Anna","Larry","Brenda","Justin","Pamela","Scott","Emma","Brandon","Nicole","Benjamin","Helen","Samuel","Samantha","Frank","Katherine","Gregory","Christine","Raymond","Debra","Alexander","Rachel","Patrick","Carolyn","Jack","Janet","Dennis","Maria","Jerry","Heather","Tyler","Diane","Aaron","Julie","Jose","Joyce","Adam","Evelyn","Nathan","Frances","Henry","Joan","Zachary","Christina")
$lastNames = @("Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts","Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes","Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper","Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson","Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes","Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross","Foster","Jimenez")
$cities = @("New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia","San Antonio","San Diego","Dallas","San Jose","Austin","Jacksonville","Fort Worth","Columbus","Charlotte","San Francisco","Indianapolis","Seattle","Denver","Washington","Boston","Nashville","El Paso","Detroit","Memphis","Portland","Oklahoma City","Las Vegas","Louisville","Baltimore","Milwaukee","Albuquerque","Tucson","Fresno","Sacramento","Mesa","Kansas City","Atlanta","Omaha","Colorado Springs","Raleigh","Miami","Virginia Beach","Oakland","Minneapolis","Tulsa","Arlington","New Orleans","Wichita")
$states = @("NY","CA","IL","TX","AZ","PA","OH","NC","WA","CO","FL","GA","NV","MA","TN","MI","MD","MO","OR","VA","MN","WI","LA","NM","KS","OK","KY","IN")
$streets = @("Main St","Oak Ave","Pine Rd","Maple Dr","Cedar Ln","Elm St","Walnut St","Sunset Blvd","Chestnut St","Hillcrest Rd","Riverside Ave","Highland Dr","Spruce St","Mulberry Ln","Park Ave","Broadway","River Rd","Forest Dr","Birch St","Sycamore Ln")

$categoryProducts = [ordered]@{
    "Electronics" = @("Wireless Earbuds","Smartphone","Bluetooth Speaker","Laptop","4K Monitor","Smartwatch","Gaming Console","Portable Charger","Wireless Mouse","Noise-Canceling Headphones")
    "Home" = @("Air Purifier","Vacuum Cleaner","Coffee Maker","Blender","Toaster Oven","Electric Kettle","Dish Set","Bed Sheets","Table Lamp","Scented Candle")
    "Beauty" = @("Moisturizing Cream","Face Serum","Shampoo","Conditioner","Hair Dryer","Perfume","Makeup Palette","Body Lotion","Facial Cleanser","Nail Polish Set")
    "Clothing" = @("Denim Jacket","Athletic Sneakers","Graphic T-Shirt","Chinos","Wool Sweater","Yoga Pants","Leather Belt","Baseball Cap","Winter Coat","Sundress")
    "Sports" = @("Running Shoes","Yoga Mat","Adjustable Dumbbells","Cycling Helmet","Tennis Racket","Basketball","Fitness Tracker","Hydration Backpack","Foam Roller","Resistance Bands")
    "Toys" = @("Building Blocks","Action Figure","Puzzle Set","Board Game","Stuffed Animal","Remote Control Car","Dollhouse","Art Kit","Science Kit","Rubik's Cube")
    "Books" = @("Mystery Novel","Cookbook","Self-Help Guide","Fantasy Epic","Historical Biography","Science Textbook","Travel Guide","Children's Storybook","Poetry Collection","Business Strategy Book")
    "Garden" = @("Planter Set","Garden Hose","Pruning Shears","Outdoor Chair","BBQ Grill","Herb Seeds","Solar Path Lights","Bird Feeder","Watering Can","Lawn Fertilizer")
    "Automotive" = @("Car Vacuum","Dash Cam","Seat Covers","Phone Mount","Tire Pressure Gauge","Jump Starter","Car Wax Kit","Floor Mats","Roof Rack","LED Headlights")
    "Health" = @("Vitamin Pack","Massage Gun","Electric Toothbrush","Water Flosser","Protein Powder","Yoga Block","Fitness Scale","First Aid Kit","Sleep Mask","Resistance Loop Set")
}
$categoryKeys = @($categoryProducts.Keys)

$customers = New-Object System.Collections.Generic.List[object]
for ($i = 1; $i -le 150; $i++) {
    $first = Get-RandomFrom $firstNames
    $last = Get-RandomFrom $lastNames
    $city = Get-RandomFrom $cities
    $state = Get-RandomFrom $states
    $address = "{0} {1}" -f $rand.Next(100,10000), (Get-RandomFrom $streets)
    $email = "{0}.{1}{2}@example.com" -f $first.ToLower(), $last.ToLower(), $rand.Next(1,100)
    $phone = "555-{0:D3}-{1:D4}" -f $rand.Next(100,1000), $rand.Next(0,10000)
    $signup = (Get-RandomDate).ToString('yyyy-MM-dd')
    $customers.Add([pscustomobject]@{
        CustomerID = $i
        FirstName = $first
        LastName = $last
        Email = $email
        Phone = $phone
        Address = $address
        City = $city
        State = $state
        Country = 'USA'
        SignupDate = $signup
    })
}

$products = New-Object System.Collections.Generic.List[object]
$productId = 1
foreach ($entry in $categoryProducts.GetEnumerator()) {
    $category = $entry.Name
    foreach ($name in $entry.Value) {
        $price = [math]::Round(5 + $rand.NextDouble() * 495, 2)
        $stock = $rand.Next(20,1001)
        $products.Add([pscustomobject]@{
            ProductID = $productId
            ProductName = $name
            Category = $category
            Price = "{0:F2}" -f $price
            StockQuantity = $stock
            Description = "$category - $name"
        })
        $productId++
    }
}
while ($products.Count -lt 120) {
    $category = Get-RandomFrom $categoryKeys
    $baseName = Get-RandomFrom $categoryProducts[$category]
    $name = "{0} {1}" -f $baseName, $rand.Next(2,10)
    $price = [math]::Round(5 + $rand.NextDouble() * 495, 2)
    $stock = $rand.Next(20,1001)
    $products.Add([pscustomobject]@{
        ProductID = $productId
        ProductName = $name
        Category = $category
        Price = "{0:F2}" -f $price
        StockQuantity = $stock
        Description = "$category - $name"
    })
    $productId++
}

$orders = New-Object System.Collections.Generic.List[object]
$orderItems = New-Object System.Collections.Generic.List[object]
$payments = New-Object System.Collections.Generic.List[object]
$orderId = 1
$orderItemId = 1
$paymentId = 1
$statusWeighted = @('Pending','Pending','Processing','Processing','Processing','Shipped','Shipped','Delivered','Delivered','Delivered','Delivered','Cancelled')
$paymentMethods = @("Credit Card","PayPal","Bank Transfer","Gift Card","Apple Pay")
$paymentStatuses = @("Completed","Pending","Failed")

for ($o = 1; $o -le 200; $o++) {
    $customer = Get-RandomFrom $customers
    $orderDate = Get-RandomDate
    $status = Get-RandomFrom $statusWeighted
    $shipAddress = "{0}, {1}, {2} USA" -f $customer.Address, $customer.City, $customer.State
    $numItems = $rand.Next(1,6)
    $selectedProducts = Get-RandomSample $products $numItems
    $total = 0.0
    foreach ($prod in $selectedProducts) {
        $qty = $rand.Next(1,5)
        $unitPrice = [double]::Parse($prod.Price)
        $subtotal = [math]::Round($qty * $unitPrice, 2)
        $total = [math]::Round($total + $subtotal, 2)
        $orderItems.Add([pscustomobject]@{
            OrderItemID = $orderItemId
            OrderID = $orderId
            ProductID = $prod.ProductID
            Quantity = $qty
            UnitPrice = "{0:F2}" -f $unitPrice
            Subtotal = "{0:F2}" -f $subtotal
        })
        $orderItemId++
    }
    $orders.Add([pscustomobject]@{
        OrderID = $orderId
        CustomerID = $customer.CustomerID
        OrderDate = $orderDate.ToString('yyyy-MM-dd')
        OrderStatus = $status
        ShippingAddress = $shipAddress
        TotalAmount = "{0:F2}" -f $total
    })
    if ($status -in @('Shipped','Delivered','Processing')) {
        $payStatus = 'Completed'
        $payAmount = $total
    } elseif ($status -eq 'Cancelled') {
        $payStatus = Get-RandomFrom @('Failed','Pending')
        $payAmount = if ($payStatus -eq 'Completed') { $total } else { 0 }
    } else {
        $payStatus = Get-RandomFrom $paymentStatuses
        $payAmount = if ($payStatus -eq 'Completed') { $total } else { [math]::Round($total * 0.5, 2) }
    }
    $payments.Add([pscustomobject]@{
        PaymentID = $paymentId
        OrderID = $orderId
        PaymentDate = $orderDate.AddDays($rand.Next(0,6)).ToString('yyyy-MM-dd')
        PaymentAmount = "{0:F2}" -f $payAmount
        PaymentMethod = Get-RandomFrom $paymentMethods
        PaymentStatus = $payStatus
    })
    $paymentId++
    $orderId++
}

$customers | Export-Csv -Path 'Customers.csv' -NoTypeInformation -Encoding UTF8
$products | Export-Csv -Path 'Products.csv' -NoTypeInformation -Encoding UTF8
$orders | Export-Csv -Path 'Orders.csv' -NoTypeInformation -Encoding UTF8
$orderItems | Export-Csv -Path 'OrderItems.csv' -NoTypeInformation -Encoding UTF8
$payments | Export-Csv -Path 'Payments.csv' -NoTypeInformation -Encoding UTF8

