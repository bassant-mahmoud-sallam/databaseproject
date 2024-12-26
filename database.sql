create database E_commerce ;
use E_commerce ;
go
create table customers (
customer_id int ,
first_name varchar(20) not null,
middle_name varchar(20) not null,
last_name varchar(20) not null,
phone int unique not null,
email varchar(30) unique ,
address varchar(40) not null ,
zip_code varchar(15),
constraint customers_pk primary key (customer_id)
);

create table categories (
category_id int ,
category_name varchar(30) not null,
constraint categories_pk primary key (category_id)
);

create table products (
product_id int ,
product_name varchar(30),
product_price decimal(8, 2) not null,
category_id int not null,
constraint products_pk primary key(product_id),
constraint products_categories_fk foreign key(category_id) references categories(category_id)
);

create table orders (
order_id int ,
order_date date not null,
total_amount decimal(10, 2) not null,
order_shipping_status varchar(40) not null,
customer_id int not null,
constraint orders_pk primary key(order_id),
constraint orders_customers_fk foreign key(customer_id) references customers(customer_id)
);

create table shipping_details (
shipping_date date ,
delivery_date date ,
shipping_address varchar(30),
delivery_address varchar(30),
shipping_company varchar(30),
order_id int,
constraint shipping_orders_fk foreign key(order_id) references orders(order_id) ,
constraint shipping_pk primary key (order_id)
);

create table payments (
payment_date date ,
payment_method varchar(20) ,
amount decimal(10, 2) ,
payment_status varchar(20),
order_id int,
constraint payments_orders foreign key(order_id) references orders(order_id),
constraint payment_pk primary key(order_id)
);

create table order_product_details (
quantity int,
total_price decimal(8,2),
order_id int,
product_id int,
constraint details_orders_fk foreign key(order_id) references orders(order_id),
constraint details_products_fk foreign key(product_id) references products(product_id),
constraint details_pk primary key(order_id , product_id)
);


CREATE SEQUENCE customer_id_seq
    START WITH 1 
    INCREMENT BY 1;

CREATE SEQUENCE order_id_seq
    START WITH 1 
    INCREMENT BY 1;

