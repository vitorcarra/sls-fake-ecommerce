create table products (
    id varchar(255),
    name varchar(255),
    manufacturer varchar(255),
    color varchar(30),
    barcode varchar(13),
    price float
);

create table users (
    id varchar(255)
    username varchar(255),
    name varchar(255),
    sex char(1),
    address varchar(255),
    mail varchar(255),
    birthdate datetime,
);


create table orders (
    order_id varchar(255),
    user_id varchar(255),
    order_date datetime,
    payment_option varchar(5), -- CC, DBT, BOL
);

create table orders_items (
    order_id varchar(255),
    product_id varchar(255),
    item_no int,    
    item_price float
);