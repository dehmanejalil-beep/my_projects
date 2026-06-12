import streamlit as st 
import pandas as pd 
from datetime import datetime 
import os 
import plotly.express as px

DATA_FILE = "budget_data.csv"

def load_data() : 
    if os.path.exists(DATA_FILE) :
        return pd.read_csv(DATA_FILE)
    
    else :
        return pd.DataFrame(columns=["type" ,"amount","statement","category","history"])

def save_data(df) :
    df.to_csv(DATA_FILE, index=False)

st.set_page_config(page_title="personal budget tracker" , layout="centered")  
st.title("your personal budget tracker")  
st.write("")

df = load_data()

st.header("add a new transaction")

col1 ,col2,col3 = st.columns(3)

with col1 :
    amount = st.number_input("amount" ,min_value=0.0,step=10.0,format="%.2f")

with col2 :
    transaction_type = st.selectbox("type",["income","expense"])

with col3 :
    category = st.selectbox("category" ,["food","housing/bills","personal development","intertanment","auther"])

description = st.text_input("additional details (statement)")
data = st.date_input("history" , datetime.now())

if st.button("add the transaction!"):
    if amount > 0 :

        new_row = {
        "history":data.strftime("%Y-%m-%d"),
        "category": category,
        "statrment" : description,
        "amount" : amount,
        "type" : transaction_type
        }
        df= pd.concat([df, pd.DataFrame([new_row])],ignore_index=True)
        save_data(df)
        st.success("transaction has been added succesfully!")
        st.rerun()

else:
        st.error("please enter an amount bigger then 0")

if not df.empty :
    st.markdown("---")
    st.header("Summary of accounts")

    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expense = df[df["type"] == "expense"]["amount"].sum()
    balance = total_income - total_expense 


    c1 ,c2 ,c3 =st.columns(3)
    c1.metric("total income" ,f"{total_income: ,.2f}")
    c2.metric("total expenses" ,f"{total_expense: ,.2f}")
    c3.metric("remaining balance" ,f"{balance: ,.2f}" , delta=balance)

    st.markdown("### Expense distribution ")
    expenses_df = df[df["type"] == "expense"]

    if not expenses_df.empty : 
        df_grouped = expenses_df.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(df_grouped , values='amount' ,names='category',
        title='where does your mony go?',
        hole=0.3, 
        color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    else :
        st.info("No expenses recorded yet to chart . Add an expense to see the distribution ")

    st.markdown("### Historical record of transactions")
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)

    st.markdown("---")
    st.header("Delete a transaction")
    delete_options = {f"Row {idx}  {row['history']}  {row['type']}  {row['amount']}": idx for idx , row in df.iterrows()}
    selected_option = st.selectbox("Select a transaction to delete! :", list(delete_options.keys()))

    if st.button("Delete selected transaction ", type="primary"):
        row_index_to_delete = delete_options[selected_option]
        df = df.drop(row_index_to_delete)
        save_data(df)
        st.success("Transaction deleted successfully!")
        st.rerun()

else :
    st.info("No transactions are recorded yet! , start by adding the first transaction above ")