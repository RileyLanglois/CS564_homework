drop table if exists Bids;
drop table if exists ItemCategories;
drop table if exists Items;
drop table if exists Users;


create table Users (
    UserID text primary key,
    Rating integer,
    Location text,
    Country text
);

create table Items (
    ItemID integer primary key,
    Name text,
    Currently float,
    Buy_Price text,
    First_Bid text,
    Number_of_Bids integer,
    Location text,
    Country text,
    Started text,
    Ends text,
    Description text,
    SellerID text references Users(UserID)
);

create table ItemCategories (
    ItemID integer references Items(ItemID),
    Category text,
    primary key (ItemID, Category)
);

create table Bids (
    UserID text references Users(UserID),
    ItemID integer references Items(ItemID),
    Time text,
    Amount float,
    primary key (UserID, ItemID, Time)
);