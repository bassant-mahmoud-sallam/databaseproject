use E_commerce;
go
-- insert values to categories and products tables
insert into categories 
values(1 , 'clothes');

insert into categories 
values(2 , 'shoes');

insert into categories 
values(3 , 'bags');

insert into products 
values(1 , 'T-shirt' , 350.00 , 1);

insert into products 
values(2 , 'jacket' , 800.00 , 1);

insert into products 
values(3 , 'pants' , 640.00 , 1);

insert into products 
values(4 , 'sports_shoes' , 640.00 , 2);

insert into products 
values(5 , 'boots' , 550.00 , 2);

insert into products 
values(6 , 'slipper' , 230.00 , 2);

insert into products 
values(7 , 'black_bag' , 420.00 , 3);

insert into products 
values(8 , 'white_bag' , 530.00 , 3);

insert into products 
values(9 , 'red_bag' , 620.00 , 3);

-- insert the all values to user make order (user 1)
insert into customers 
values(1 , 'asmaa' , 'ahmed' , 'mohammed' , 01015962, 'asmaaf@mail.com' , 'Egypt cairo' , '#w567');
insert into orders
values(1 , '2024-8-30' , 1350.00 , 'Delivered' ,1);
insert into order_product_details 
values(1 , 800.00 , 1 , 2);
insert into order_product_details 
values(1 , 550.00 , 1 , 5);
insert into payments 
values('2024-9-15' , 'cash' , 1350.00 , 'Paid' , 1);
insert into shipping_details
values('2024-9-15' , '2024-9-15' , 'Egypt cairo' , 'Egypt cairo' , 'company_one' , 1);

-- insert the all values to user make order (user 2)
insert into customers 
values(2 , 'omar' , 'ali' , 'ahmed' , 01248963 , 'omaro@mail.com' , 'Egypt alexndria' , '#a146');
insert into orders
values(2 , '2024-7-20' , 1760.00 , 'Delivered' ,2);
insert into order_product_details 
values(2 , 700.00 , 2 , 1);
insert into order_product_details 
values(1 , 640.00 , 2 , 4);
insert into order_product_details 
values(1 , 420.00 , 2 , 7);
insert into payments 
values('2024-8-1' , 'Bank Transfers' , 1760.00 , 'Paid' , 2);
insert into shipping_details
values('2024-7-30' , '2024-8-1' , 'Egypt cairo' , 'Egypt alexndria' , 'company_two' , 2);

-- insert the all values to user make order (user 3)
insert into customers 
values(3 , 'sara' , 'mohammed' , 'ali' , 01189623 , 'saraa@mail.com' , 'Egypt menofia' , '#m783');
insert into orders
values(3 , '2024-7-3' , 1170.00 , 'Cancelled' ,3);
insert into order_product_details 
values(1 , 640.00 , 3 , 3);
insert into order_product_details 
values(1 , 530.00 , 3 , 8);
insert into payments 
values(null , null ,0,'Cancelled' , 3);
insert into shipping_details
values(null , null , 'Egypt cairo' , 'Egypt menofia' , 'company_three' , 3);

-- start autoincreament from 4
ALTER SEQUENCE customer_id_seq RESTART WITH 4;
ALTER SEQUENCE order_id_seq RESTART WITH 4;

