$random = [System.Random]::new(42)
$baseDate = Get-Date "2020-01-01"

$firstNames = "Emma","Liam","Olivia","Noah","Ava","Ethan","Sophia","Mason","Isabella","Logan","Mia","Lucas","Charlotte","Jackson","Amelia","Aiden","Harper","Elijah","Evelyn","Oliver","Abigail","Jacob","Emily","Michael","Elizabeth","Daniel","Sofia","Henry","Avery","Sebastian","Ella","Jack","Scarlett","Alexander","Grace","Carter","Chloe","Wyatt","Victoria","Jayden","Riley","Leo","Aria","Gabriel","Lily","Anthony","Penelope","Isaac","Layla","Grayson","Nora","Hudson","Zoey","Matthew","Mila","Ezra","Hannah","Lincoln","Lillian","Luke","Addison","Julian","Eleanor","Owen","Natalie","Caleb","Luna","Ryan","Savannah","Nathan","Brooklyn","Thomas","Leah","Charles","Zoe","Christopher","Stella","Jaxon","Hazel","Miles","Ellie","Isaiah","Paisley","Andrew","Audrey","Joshua","Skylar","Jose","Violet","Christian","Claire","Hunter","Bella","Eli","Aurora","Jonathan","Lucy","Connor","Anna"
$lastNames = "Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez","Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris","Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen","Hill","Flores","Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts","Gomez","Phillips","Evans","Turner","Diaz","Parker","Cruz","Edwards","Collins","Reyes","Stewart","Morris","Morales","Murphy","Cook","Rogers","Gutierrez","Ortiz","Morgan","Cooper","Peterson","Bailey","Reed","Kelly","Howard","Ramos","Kim","Cox","Ward","Richardson","Watson","Brooks","Chavez","Wood","James","Bennett","Gray","Mendoza","Ruiz","Hughes","Price","Alvarez","Castillo","Sanders","Patel","Myers","Long","Ross"
$streets = "Maple St","Oak Ave","Pine Rd","Cedar Ln","Elm St","Walnut Dr","Birch Ct","Chestnut Blvd","Willow Way","Aspen Cir","Highland Rd","River St","Sunset Ave","Forest Dr","Lakeside Blvd","Hillcrest Rd","Sycamore St","Meadow Ln","Park Ave","Spruce St"
$cities = "Seattle","Austin","Denver","Boston","Chicago","Phoenix","San Diego","Portland","Atlanta","Dallas","San Jose","Miami","Orlando","Nashville","Charlotte","Columbus","Indianapolis","Detroit","Minneapolis","Tampa","Raleigh","Baltimore","Cincinnati","Cleveland","Pittsburgh","Kansas City","Salt Lake City","Las Vegas","Richmond","St. Louis","Milwaukee","New Orleans","Memphis","Hartford","Providence","Albany","Sacramento","San Antonio","Boulder","Madison"
$states = "WA","TX","CO","MA","IL","AZ","CA","OR","GA","NC","FL","OH","MI","MN","UT","NV","VA","MO","WI","LA","TN","CT","RI","NY","PA","MD"

function Get-RandomDate {
    param([int]$maxDays)
    $days = $random.Next(0,$maxDays+1)
    return $baseDate.AddDays($days).ToString("yyyy-MM-dd")
}

function New-WeightedList {
    param(
        [string[]]$values,
        [int[]]$weights
    )
    $list = New-Object System.Collections.Generic.List[string]
    for ($i=0; $i -lt $values.Count; $i++) {
        for ($w=0; $w -lt $weights[$i]; $w++) {
            $list.Add($values[$i])
        }
    }
    return $list
}

$customers = @()
for ($cid=1; $cid -le 100; $cid++) {
    $fn = $firstNames[$random.Next(0,$firstNames.Count)]
    $ln = $lastNames[$random.Next(0,$lastNames.Count)]
    $email = "{0}.{1}{2}@example.com" -f $fn.ToLower(), $ln.ToLower(), $cid
    $phone = "555-{0}" -f $random.Next(1000000,9999999)
    $addr = "{0} {1}" -f $random.Next(100,999), $streets[$random.Next(0,$streets.Count)]
    $city = $cities[$random.Next(0,$cities.Count)]
    $state = $states[$random.Next(0,$states.Count)]
    $customers += [pscustomobject]@{
        CustomerID=$cid
        FirstName=$fn
        LastName=$ln
        Email=$email
        Phone=$phone
        Address=$addr
        City=$city
        State=$state
        Country="USA"
        SignupDate=Get-RandomDate -maxDays 1825
    }
}

$categories = "Electronics","Home","Fashion","Sports","Beauty","Toys","Books","Garden","Automotive","Office"
$products = @()
for ($prodId=1; $prodId -le 100; $prodId++) {
    $cat = $categories[$random.Next(0,$categories.Count)]
    $price = [math]::Round(($random.NextDouble()*495)+5,2)
    $products += [pscustomobject]@{
        ProductID=$prodId
        ProductName="{0} Item {1}" -f $cat,$prodId
        Category=$cat
        Price=[math]::Round($price,2)
        StockQuantity=$random.Next(10,501)
        Description="High-quality {0} product #{1}" -f $cat.ToLower(),$prodId
    }
}

$orderStatuses = New-WeightedList -values @("Pending","Processing","Shipped","Delivered","Cancelled") -weights @(10,20,30,35,5)

$orders = @()
$orderTotals = @{}
for ($oid=1; $oid -le 120; $oid++) {
    $cust = $customers[$random.Next(0,$customers.Count)]
    $status = $orderStatuses[$random.Next(0,$orderStatuses.Count)]
    $shipAddr = "{0}, {1}, {2}" -f $cust.Address, $cust.City, $cust.State
    $orders += [pscustomobject]@{
        OrderID=$oid
        CustomerID=$cust.CustomerID
        OrderDate=Get-RandomDate -maxDays 1825
        OrderStatus=$status
        ShippingAddress=$shipAddr
        TotalAmount="0.00"
    }
    $orderTotals[$oid] = 0.0
}

$orderItems = @()
$orderItemId = 1
for ($oid=1; $oid -le 120; $oid++) {
    $numItems = $random.Next(1,5)
    $productSample = $products | Get-Random -Count $numItems
    $orderSubtotal = 0.0
    foreach ($prod in $productSample) {
        $qty = $random.Next(1,6)
        $unitPrice = [double]$prod.Price
        $subtotal = [math]::Round($qty * $unitPrice, 2)
        $orderSubtotal += $subtotal
        $orderItems += [pscustomobject]@{
            OrderItemID=$orderItemId
            OrderID=$oid
            ProductID=$prod.ProductID
            Quantity=$qty
            UnitPrice="{0:F2}" -f $unitPrice
            Subtotal="{0:F2}" -f $subtotal
        }
        $orderItemId++
    }
    $orderTotals[$oid] = [math]::Round($orderTotals[$oid] + $orderSubtotal, 2)
}

for ($i=0; $i -lt $orders.Count; $i++) {
    $oid = $orders[$i].OrderID
    $orders[$i].TotalAmount = "{0:F2}" -f $orderTotals[$oid]
}

$paymentMethods = "Credit Card","PayPal","Gift Card","Bank Transfer","Apple Pay"
$paymentStatuses = New-WeightedList -values @("Completed","Pending","Failed","Refunded") -weights @(70,15,10,5)

$payments = @()
for ($oid=1; $oid -le 120; $oid++) {
    $payments += [pscustomobject]@{
        PaymentID=$oid
        OrderID=$oid
        PaymentDate=Get-RandomDate -maxDays 1825
        PaymentAmount="{0:F2}" -f $orderTotals[$oid]
        PaymentMethod=$paymentMethods[$random.Next(0,$paymentMethods.Count)]
        PaymentStatus=$paymentStatuses[$random.Next(0,$paymentStatuses.Count)]
    }
}

$customers | Export-Csv -Path Customers.csv -NoTypeInformation
$products | Export-Csv -Path Products.csv -NoTypeInformation
$orders | Export-Csv -Path Orders.csv -NoTypeInformation
$orderItems | Export-Csv -Path OrderItems.csv -NoTypeInformation
$payments | Export-Csv -Path Payments.csv -NoTypeInformation
