import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="PhonePe Transaction Insights",
    layout="wide"
)


with open("india_states.geojson", "r", encoding="utf-8") as file:
    geo_data = json.load(file)


# MySQL Connection
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)


# Dashboard Title
st.header("PhonePe Transaction Insights")
st.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Analysis"]
)
if page == "Home":
    st.header("Transaction Overview")

    # Load transaction data
    query = """
    SELECT State,Year,Quarter,
    SUM(Transaction_Count) AS Transaction_Count,
    SUM(Transaction_Amount) AS Total_Transaction_Amount
    FROM Map_Transaction
    GROUP BY State,Year,Quarter
    """
    df = pd.read_sql(query, conn)
    # Create two columns for filters
    col1, col2 = st.columns(2)
    with col1:
        years = sorted(df["Year"].unique())
        selected_year = st.selectbox("Select Year", years)
    with col2:
        quarters = sorted(df["Quarter"].unique())
        selected_quarter = st.selectbox("Select Quarter", quarters)
# Filter data
    df = df[
    (df["Year"] == selected_year) &
    (df["Quarter"] == selected_quarter)
]
    # Calculate summary values
    total_transactions = df["Transaction_Count"].sum()
    total_amount = df["Total_Transaction_Amount"].sum()
    average_amount = total_amount / total_transactions if total_transactions > 0 else 0

    # Display summary cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Transactions", f"{total_transactions:,.0f}")
    col2.metric("Total Transaction Amount",
            f"₹{total_amount:,.0f}")
    col3.metric("Average Transaction Amount",
            f"₹{average_amount:,.2f}")

    # Convert state names into GeoJSON format
    df["State"] = df["State"].str.replace("-", " ", regex=False).str.title()

    # Correct special state names
    df["State"] = df["State"].replace({
        "Andaman & Nicobar Islands": "Andaman & Nicobar",
        "Dadra And Nagar Haveli And Daman And Diu":
        "Dadra and Nagar Haveli and Daman and Diu"
    })

    # Create India Map
    fig = px.choropleth(
        df,
        geojson=geo_data,
        featureidkey="properties.ST_NM",
        locations="State",
        color="Total_Transaction_Amount",
        color_continuous_scale="Reds",
        hover_name="State",
        hover_data={"Total_Transaction_Amount": ":,.0f"}
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    fig.update_layout(
        title="State-wise Transaction Amount",
        height=650
    )
    st.plotly_chart(fig, width="stretch")

elif page == "Analysis":

    st.header("Business Case Study Analysis")

    case_study = st.selectbox(
        "Choose Case Study",
        [
            "Decoding Transaction Dynamics on PhonePe",
            "Transaction Market Expansion",
            "User Engagement and Growth",
            "Transaction Analysis Across States and Districts",
            "Merchant Registration Analysis"
        ]
    )

    if case_study == "Decoding Transaction Dynamics on PhonePe":

        # Question 1: What are the different transaction types?
        st.subheader("1. Distribution of Transaction Types")

        query1 = """
        SELECT Transaction_Type,
            SUM(Transaction_Count) AS Total_Transactions
        FROM Agg_Transaction
        GROUP BY Transaction_Type
        """

        df1 = pd.read_sql(query1, conn)

        fig1 = px.pie(
            df1,
            names="Transaction_Type",
            values="Total_Transactions",
            title="Transaction Type Distribution",
            hole=0.4
        )
        st.plotly_chart(
        fig1,
        width="stretch",
        config={"staticPlot": True}
    )


        # Question 2: Which transaction type has the highest transactions?
        st.subheader("2. Total Transactions by Payment Category")

        query2 = """
        SELECT Transaction_Type,
            SUM(Transaction_Count) AS Total_Transactions
        FROM Agg_Transaction
        GROUP BY Transaction_Type
        ORDER BY Total_Transactions DESC
        """

        df2 = pd.read_sql(query2, conn)

        fig2 = px.bar(
            df2,
            x="Transaction_Type",
            y="Total_Transactions",
            title="Transactions by Payment Category"
        )
        st.plotly_chart(
                fig2,
                width="stretch",
                config={"staticPlot": True}
        )
        


        # Question 3: Which states have the highest transaction count?
        st.subheader("3. Top 10 States by Transaction Count")

        query3 = """
        SELECT State,
            SUM(Transaction_Count) AS Total_Transactions
        FROM Agg_Transaction
        GROUP BY State
        ORDER BY Total_Transactions DESC
        LIMIT 10
        """

        df3 = pd.read_sql(query3, conn)

        fig3 = px.bar(
            df3,
            x="State",
            y="Total_Transactions",
            title="Top 10 States by Transactions"
        )
        st.plotly_chart(
                fig3,
                width="stretch",
                config={"staticPlot": True}
        )
        


        # Question 4: How do payment categories perform across states?
        st.subheader("4. State-wise Payment Category Performance")

        query4 = """
        SELECT State, Transaction_Type,
            SUM(Transaction_Count) AS Total_Transactions
        FROM Agg_Transaction
        GROUP BY State, Transaction_Type
        """

        df4 = pd.read_sql(query4, conn)

        fig4 = px.bar(
            df4,
            x="State",
            y="Total_Transactions",
            color="Transaction_Type",
            barmode="stack",
            title="State-wise Transaction Category Performance"
        )
        st.plotly_chart(
                fig4,
                width="stretch",
                config={"staticPlot": True}
        )
        


        # Question 5: How do transactions change over time?
        st.subheader("5. Quarterly Transaction Trend")

        query5 = """
        SELECT Year, Quarter,
            SUM(Transaction_Count) AS Total_Transactions
        FROM Agg_Transaction
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter
        """

        df5 = pd.read_sql(query5, conn)

        df5["Period"] = (
            df5["Year"].astype(str) + " Q" +
            df5["Quarter"].astype(str)
        )

        fig5 = px.line(
            df5,
            x="Period",
            y="Total_Transactions",
            markers=True,
            title="Quarterly Transaction Trend"
        )
        st.plotly_chart(
                fig5,
                width="stretch",
                config={"staticPlot": True}
        )
        


    elif case_study == "Transaction Market Expansion":

            # Question 1: Which are the top 10 districts by transaction amount?
        st.subheader("1. Top 10 Districts by Transaction Amount")

        query1 = """
        SELECT State, District_Name,
            SUM(Transaction_Amount) AS Total_Transaction_Amount
        FROM Map_Transaction
        GROUP BY State, District_Name
        ORDER BY Total_Transaction_Amount DESC
        LIMIT 10
        """

        df1 = pd.read_sql(query1, conn)

        fig1 = px.bar(
            df1,
            x="District_Name",
            y="Total_Transaction_Amount",
            title="Top 10 Districts by Transaction Amount",
            hover_data=["State"]
        )
        st.plotly_chart(fig1, width="stretch", config={"staticPlot": True})


        # Question 2: Which are the top 10 states by transaction amount?
        st.subheader("2. Top 10 States by Transaction Amount")

        query2 = """
        SELECT State,
            SUM(Transaction_Amount) AS Total_Transaction_Amount
        FROM Map_Transaction
        GROUP BY State
        ORDER BY Total_Transaction_Amount DESC
        LIMIT 10
        """

        df2 = pd.read_sql(query2, conn)

        fig2 = px.pie(
            df2,
            names="State",
            values="Total_Transaction_Amount",
            hole=0.4,
            title="Top 10 States by Transaction Amount"
        )

        st.plotly_chart(
            fig2,
            width="stretch",
            config={"staticPlot": True}
        )



        # Question 3: Which are the top 10 districts by transaction count?
        st.subheader("3. Top 10 Districts by Transaction Count")

        query3 = """
        SELECT State, District_Name,
            SUM(Transaction_Count) AS Total_Transactions
        FROM Map_Transaction
        GROUP BY State, District_Name
        ORDER BY Total_Transactions DESC
        LIMIT 10
        """

        df3 = pd.read_sql(query3, conn)

        fig3 = px.bar(
            df3,
            x="District_Name",
            y="Total_Transactions",
            title="Top 10 Districts by Transaction Count",
            hover_data=["State"]
        )
        st.plotly_chart(fig3, width="stretch", config={"staticPlot": True})


        # Question 4: Which states have the highest average transaction amount?
        st.subheader("4. Top 10 States by Average Transaction Amount")

        query4 = """
        SELECT State,
            SUM(Transaction_Amount) / SUM(Transaction_Count)
            AS Average_Transaction_Amount
        FROM Map_Transaction
        GROUP BY State
        ORDER BY Average_Transaction_Amount DESC
        LIMIT 10
        """

        df4 = pd.read_sql(query4, conn)

        fig4 = px.bar(
            df4,
            x="State",
            y="Average_Transaction_Amount",
            title="Top 10 States by Average Transaction Amount"
        )
        st.plotly_chart(fig4, width="stretch", config={"staticPlot": True})


        # Question 5: How does transaction amount change over time?
        st.subheader("5. Quarterly Transaction Amount Trend")

        query5 = """
        SELECT Year, Quarter,
            SUM(Transaction_Amount) AS Total_Transaction_Amount
        FROM Map_Transaction
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter
        """

        df5 = pd.read_sql(query5, conn)

        df5["Period"] = (
            df5["Year"].astype(str) + " Q" +
            df5["Quarter"].astype(str)
        )

        fig5 = px.line(
            df5,
            x="Period",
            y="Total_Transaction_Amount",
            markers=True,
            title="Quarterly Transaction Amount Trend"
        )
        st.plotly_chart(fig5, width="stretch", config={"staticPlot": True})


    elif case_study == "User Engagement and Growth":

            # Question 1: Top 10 states by registered users
        st.subheader("1. Top 10 States by Registered Users")

        query1 = """
        SELECT State,
            SUM(Registered_User) AS Total_Registered_Users
        FROM Agg_User
        GROUP BY State
        ORDER BY Total_Registered_Users DESC
        LIMIT 10
        """

        df1 = pd.read_sql(query1, conn)

        fig1 = px.bar(
            df1,
            x="State",
            y="Total_Registered_Users",
            title="Top 10 States by Registered Users"
        )
        st.plotly_chart(fig1, width="stretch", config={"staticPlot": True})


        # Question 2: Top 10 districts by registered users
        st.subheader("2. Top 10 Districts by Registered Users")

        query2 = """
        SELECT State, District_name,
            SUM(Registered_User) AS Total_Registered_Users
        FROM Map_User
        GROUP BY State, District_name
        ORDER BY Total_Registered_Users DESC
        LIMIT 10
        """

        df2 = pd.read_sql(query2, conn)

        fig2 = px.pie(
            df2,
            names="District_name",
            values="Total_Registered_Users",
            hole=0.4,
            title="Top 10 Districts by Registered Users"
        )

        st.plotly_chart(
            fig2,
            width="stretch",
            config={"staticPlot": True}
        )


        # Question 3: Registered users across years and quarters
        st.subheader("3. Quarterly Registered User Growth")

        query3 = """
        SELECT Year, Quarter,
            SUM(Registered_User) AS Total_Registered_Users
        FROM Agg_User
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter
        """

        df3 = pd.read_sql(query3, conn)

        df3["Period"] = (
            df3["Year"].astype(str) + " Q" +
            df3["Quarter"].astype(str)
        )

        fig3 = px.line(
            df3,
            x="Period",
            y="Total_Registered_Users",
            markers=True,
            title="Quarterly Registered Users"
        )
        st.plotly_chart(fig3, width="stretch", config={"staticPlot": True})


        # Question 4: Top 10 states by registered merchants
        st.subheader("4. Top 10 States by Registered Merchants")

        query4 = """
        SELECT State,
            SUM(Registered_Merchant_count) AS Total_Registered_Merchants
        FROM Agg_Merchant
        GROUP BY State
        ORDER BY Total_Registered_Merchants DESC
        LIMIT 10
        """

        df4 = pd.read_sql(query4, conn)

        fig4 = px.bar(
            df4,
            x="State",
            y="Total_Registered_Merchants",
            title="Top 10 States by Registered Merchants"
        )
        st.plotly_chart(fig4, width="stretch", config={"staticPlot": True})


        # Question 5: Average registered merchants by state
        st.subheader("5. Average Registered Merchants by State")

        query5 = """
        SELECT State,
            AVG(Registered_Merchant_count) AS Average_Registered_Merchants
        FROM Agg_Merchant
        GROUP BY State
        ORDER BY Average_Registered_Merchants DESC
        LIMIT 10
        """

        df5 = pd.read_sql(query5, conn)

        fig5 = px.pie(
            df5,
            names="State",
            values="Average_Registered_Merchants",
            title="Average Registered Merchants by State"
        )

        st.plotly_chart(
            fig5,
            width="stretch",
            config={"staticPlot": True}
        )


    elif case_study == "Transaction Analysis Across States and Districts":

            # Question 1: Top 10 states by registered users and merchants
        st.subheader("1. State-wise Registered Users and Merchants")

        query1 = """
        SELECT
            U.State,
            SUM(U.Registered_User) AS Total_Registered_Users,
            SUM(M.Registered_Merchant_count) AS Total_Registered_Merchants
        FROM Agg_User U
        JOIN Agg_Merchant M
            ON U.State = M.State
            AND U.Year = M.Year
            AND U.Quarter = M.Quarter
        GROUP BY U.State
        ORDER BY Total_Registered_Users DESC
        LIMIT 10
        """

        df1 = pd.read_sql(query1, conn)

        fig1 = px.bar(
            df1,
            x="State",
            y=["Total_Registered_Users", "Total_Registered_Merchants"],
            barmode="group",
            title="Top 10 States: Users and Merchants"
        )
        st.plotly_chart(fig1, width="stretch", config={"staticPlot": True})


        # Question 2: Average transaction amount by state
        st.subheader("2. Top 10 States by Average Transaction Amount")

        query2 = """
        SELECT State,
            AVG(Transaction_Amount) AS Average_Transaction_Amount
        FROM Map_Transaction
        GROUP BY State
        ORDER BY Average_Transaction_Amount DESC
        LIMIT 10
        """

        df2 = pd.read_sql(query2, conn)

        fig2 = px.pie(
            df2,
            names="State",
            values="Average_Transaction_Amount",
            hole=0.4,
            title="Average Transaction Amount by State"
        )

        st.plotly_chart(
            fig2,
            width="stretch",
            config={"staticPlot": True}
        )


        # Question 3: Highest yearly transaction amount
        st.subheader("3. Year-wise Transaction Amount")

        query3 = """
        SELECT Year,
            SUM(Transaction_Amount) AS Total_Transaction_Amount
        FROM Map_Transaction
        GROUP BY Year
        ORDER BY Year
        """

        df3 = pd.read_sql(query3, conn)

        fig3 = px.line(
            df3,
            x="Year",
            y="Total_Transaction_Amount",
            markers=True,
            title="Year-wise Transaction Amount"
        )

        st.plotly_chart(
            fig3,
            width="stretch",
            config={"staticPlot": True}
        )


        # Question 4: Top 10 districts by transaction amount in 2025
        st.subheader("4. Top 10 Districts by Transaction Amount in 2025")

        query4 = """
        SELECT State, District_name, Year,
            SUM(Transaction_Amount) AS Total_Transaction_Amount
        FROM Map_Transaction
        WHERE Year = 2025
        GROUP BY State, District_name, Year
        ORDER BY Total_Transaction_Amount DESC
        LIMIT 10
        """

        df4 = pd.read_sql(query4, conn)

        fig4 = px.bar(
            df4,
            x="District_name",
            y="Total_Transaction_Amount",
            hover_data=["State"],
            title="Top 10 Districts by Transaction Amount in 2025"
        )
        st.plotly_chart(fig4, width="stretch", config={"staticPlot": True})


        # Question 5: State-wise transaction count
        st.subheader("5. Top 10 States by Transaction Count")

        query5 = """
        SELECT State,
            SUM(Transaction_Count) AS Total_Transactions
        FROM Agg_Transaction
        GROUP BY State
        ORDER BY Total_Transactions DESC
        LIMIT 10
        """

        df5 = pd.read_sql(query5, conn)

        fig5 = px.pie(
            df5,
            names="State",
            values="Total_Transactions",
            title="Top 10 States by Transaction Count"
        )

        st.plotly_chart(
            fig5,
            width="stretch",
            config={"staticPlot": True}
        )


    elif case_study == "Merchant Registration Analysis":

            # Question 1: Top 10 districts by registered merchants
        st.subheader("1. Top 10 Districts by Registered Merchants")

        query1 = """
        SELECT State, District_name,
            SUM(Registered_merchant) AS Total_Registered_Merchants
        FROM Map_Merchant
        GROUP BY State, District_name
        ORDER BY Total_Registered_Merchants DESC
        LIMIT 10
        """

        df1 = pd.read_sql(query1, conn)

        fig1 = px.bar(
            df1,
            x="District_name",
            y="Total_Registered_Merchants",
            hover_data=["State"],
            title="Top 10 Districts by Registered Merchants"
        )
        st.plotly_chart(fig1, width="stretch", config={"staticPlot": True})


        # Question 2: Merchant counts across years and quarters
        st.subheader("2. Quarterly Registered Merchant Trend")

        query2 = """
        SELECT Year, Quarter,
            SUM(Registered_Merchant_count) AS Total_Registered_Merchants
        FROM Agg_Merchant
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter
        """

        df2 = pd.read_sql(query2, conn)

        df2["Period"] = (
            df2["Year"].astype(str) + " Q" +
            df2["Quarter"].astype(str)
        )

        fig2 = px.line(
            df2,
            x="Period",
            y="Total_Registered_Merchants",
            markers=True,
            title="Quarterly Registered Merchants"
        )
        st.plotly_chart(fig2, width="stretch", config={"staticPlot": True})


        # Question 3: Year-wise registered merchants
        st.subheader("3. Year-wise Registered Merchants")

        query3 = """
        SELECT Year,
            SUM(Registered_Merchant_count) AS Total_Registered_Merchants
        FROM Agg_Merchant
        GROUP BY Year
        ORDER BY Year
        """

        df3 = pd.read_sql(query3, conn)

        fig3 = px.pie(
            df3,
            names="Year",
            values="Total_Registered_Merchants",
            hole=0.4,
            title="Year-wise Registered Merchants"
        )

        st.plotly_chart(
            fig3,
            width="stretch",
            config={"staticPlot": True}
        )


        # Question 4: Number of districts represented in Top_Merchant
        st.subheader("4. Top 10 States by Represented District Count")

        query4 = """
        SELECT State,
            COUNT(DISTINCT District_name) AS Total_Districts
        FROM Top_Merchant
        GROUP BY State
        ORDER BY Total_Districts DESC
        LIMIT 10
        """

        df4 = pd.read_sql(query4, conn)

        fig4 = px.bar(
            df4,
            x="State",
            y="Total_Districts",
            title="Districts Represented in Top Merchant Data"
        )
        st.plotly_chart(fig4, width="stretch", config={"staticPlot": True})


        # Question 5: Top 10 districts by merchant count
        st.subheader("5. Top 10 Districts by Merchant Count")

        query5 = """
        SELECT State, District_name,
            SUM(Registered_merchant) AS Total_Registered_Merchants
        FROM Top_Merchant
        GROUP BY State, District_name
        ORDER BY Total_Registered_Merchants DESC
        LIMIT 10
        """

        df5 = pd.read_sql(query5, conn)

        fig5 = px.bar(
            df5,
            x="District_name",
            y="Total_Registered_Merchants",
            hover_data=["State"],
            title="Top 10 Districts by Merchant Count"
        )
        st.plotly_chart(fig5, width="stretch", config={"staticPlot": True})

