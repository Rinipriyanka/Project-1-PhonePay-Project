/*create database Phonepe_Pulse;*/
use Phonepe_Pulse;

/*1. Decoding Transaction Dynamics on Phonepe*/
/*A.Different transaction categories available in PhonePe?*/
/*select * from agg_transaction limit 5;
select Transaction_Type,sum(Transaction_Count) as Total_Transaction from agg_transaction 
group by Transaction_Type
order by Total_Transaction desc;*/

/* B.Which states have the highest total transaction count?*/
/*select State,sum(Transaction_Count) as Total_Transaction from agg_transaction
group by State 
order by Total_Transaction desc;*/

/*C. What is the total transaction count for each transaction type across different states?*/
/*select State,Transaction_Type, sum(Transaction_Count) as Total_Transactions from Agg_Transaction
group by State, Transaction_Type
order by State, Total_Transactions desc limit 20;*/

/*D.How have transaction counts changed across different quarters and years?*/
/*select Year, Quarter,sum(Transaction_Count) as Total_Transactions from Agg_Transaction
group by Year, Quarter
order by Year, Quarter;*/

/*E.Which year and quarter recorded the highest transaction volume?*/
/*select Year,Quarter,sum(Transaction_Count) as Total_Transactions from Agg_Transaction
group by Year, Quarter
order by Total_Transactions desc limit 1;*/

/* 2.Transaction Analysis for Market Expansion*/
/*A.Which districts have the highest total transaction amount?*/
/*select * from map_transaction limit 5;
select State,District_Name,sum(Transaction_amount) as Total_Transaction_amount from map_transaction
group by State, District_Name
order by Total_Transaction_amount desc limit 10;*/

/*B.Which states generate the highest total transaction amount?*/
/*select State,sum(Transaction_Amount) AS Total_Transaction_Amount from Map_Transaction
group by State
order by Total_Transaction_Amount desc limit 10;*/

/*C.Which districts have the highest transaction count?*/
/*select State, District_Name,sum(Transaction_Count) AS Total_Transactions_count from Map_Transaction
group by State, District_Name
order by Total_Transactions_count desc limit 10;*/

/*D.Which states have the highest average transaction amount per transaction?*/
/*select State,sum(Transaction_Amount) / sum(Transaction_Count) AS Average_Transaction_Amount from Map_Transaction
group by State
order by Average_Transaction_Amount desc limit 10;*/

/*E.How has the total transaction amount changed across different years and quarters?*/
/*select Year,Quarter,sum(Transaction_Amount) AS Total_Transaction_Amount from Map_Transaction
group by Year, Quarter
order by Year, Quarter;*/

/*3.User Engagement and Growth Strategy*/
/*A.Which states have the highest number of registered users?*/
/*select * from map_user limit 5;*/
/*select State,sum(Registered_User) as Total_Registered_User from agg_user
group by State
order by Total_Registered_User desc limit 5;*/

/*B.Which districts have the highest number of registered users?*/
/*Select State,District_Name,sum(Registered_User) as Total_Registered_User from map_user
group by State,District_Name
order by Total_Registered_user desc limit 5;*/

/*C.How have registered users grown across different years and quarters?*/
/*select Year,Quarter,sum(Registered_User) as Total_Registered_User from agg_user
group by Year,quarter
order by Year,Quarter desc;*/

/*D.Which states have the highest number of registered merchants?*/
/*select * from agg_merchant limit 5;*/
/*select State,sum(Registered_Merchant_count) as Total_Registered_Merchant from agg_merchant
group by State
order by Total_Registered_Merchant desc limit 5;*/

/*E.Which states have the highest average number of registered merchants per quarter?*/
/*select State,Quarter,sum(Registered_Merchant_count) as Total_Registered_Merchant,avg(Registered_Merchant_count) as Average_Registered_Merchant_count
from agg_merchant
group by State, quarter
order by Average_Registered_Merchant_count desc;*/

/*4.Transaction Analysis Across States and Districts*/
/*A.How many districts are available in each state in the Map_Trans dataset?*/
/*select State,count(distinct District_Name) AS Total_Districts
from Map_Transaction
group by State
order by Total_Districts desc;*/

/*B.Which states have the highest total number of registered users and merchants?*/
/*select U.State,SUM(U.Registered_User) AS Total_Registered_Users,SUM(M.Registered_Merchant_count) AS Total_Registered_Merchants
from Agg_User U
join Agg_Merchant M
    on U.State = M.State
    and U.Year = M.Year
    and U.Quarter = M.Quarter
group by U.State
order by Total_Registered_Users DESC
limit 10;*/

/*C.Which states have the highest average transaction amount?*/
/*select State,avg(Transaction_Amount) AS Average_Transaction_Amount
FROM Map_Transaction
group by State
order by Average_Transaction_Amount desc
limit 10;*/

/*D.Which year recorded the highest total transaction amount?*/
/*select Year,SUM(Transaction_Amount) AS Total_Transaction_Amount
FROM Map_Transaction
group by Year
order by Total_Transaction_Amount desc
limit 1;*/

/*E.Which districts have the highest total transaction amount in a selected year?*/
/*select State,District_Name,Year,SUM(Transaction_Amount) AS Total_Transaction_Amount
from Map_Transaction
where Year = 2025
group by State, District_Name, Year
order by Total_Transaction_Amount DESC
LIMIT 10;*/

/*5.Merchant Registration Analysis*/
/*A.Which districts have the highest number of registered merchants?*/
/*select State,District_Name,SUM(Registered_Merchant) AS Total_Registered_Merchants
from Map_Merchant
group by State, District_Name
order by Total_Registered_Merchants DESC limit 10;*/

/*B.How have registered merchants changed across different years and quarters?*/
/*select Year,Quarter,SUM(Registered_Merchant_count) AS Total_Registered_Merchants
FROM Agg_Merchant
group by Year, Quarter
order by Year, Quarter;*/

/*C.Which districts have the highest registered merchant counts according to the Top Merchant dataset?*/
/*select State, District_Name,SUM(Registered_Merchant) AS Total_Registered_Merchants
from Top_Merchant group by State, District_Name
order by Total_Registered_Merchants DESC
LIMIT 10;*/

select * from Top_Transaction;
/*D.how many registered merchants are present relative to the registered user count in each district.*/
SELECT
    M.State,
    M.District_Name,
    M.Registered_merchant,
    U.Registered_Users,
    ROUND(
        M.Registered_merchant * 100.0 /
        U.Registered_Users, 2
    ) AS Merchant_User_Ratio_Percentage
FROM Top_Merchant M
JOIN Top_User U
    ON M.State = U.State
    AND M.Year = U.Year
    AND M.Quarter = U.Quarter
    AND M.District_Name = U.District_Name
WHERE U.Registered_Users > 0
ORDER BY Merchant_User_Ratio_Percentage DESC
LIMIT 10;

/*5.Which year and quarter recorded the highest average registered merchant count per district?*/
SELECT
    Year,
    Quarter,
    AVG(Registered_merchant) AS Average_Merchant_Count
FROM Top_Merchant
GROUP BY Year, Quarter
ORDER BY Average_Merchant_Count DESC
LIMIT 1;