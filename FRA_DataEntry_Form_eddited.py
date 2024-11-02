import mysql.connector
import streamlit as st
import pandas as pd
st.set_page_config(layout='wide')
# MySQL connection setup
USERNAME = 'root'  # Your MySQL username
PASSWORD = '1234'    # Your MySQL password

def create_connection():
    try:
        con = mysql.connector.connect(
            host='localhost',        # Your MySQL server host
            user=USERNAME,           # Your MySQL username
            password=PASSWORD,       # Your MySQL password
            database='frtc'          # Your MySQL database name
        )
        return con
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Fetch all records from the table
def fetch_data(cur):
    cur.execute("SELECT * FROM fradata2024")
    return cur.fetchall()

# Insert new data into the table
def insert_data(con, cur, data):
    insert_query = """
    INSERT INTO fradata2024 (col_no, row_no, plot_number, plot_id, tree_no, bearing, distance, 
    species_code, species_name, dbh_cm, quality_class, crown_class, sample_type, tree_ht_m, 
    crown_ht_m, tree_ht_base, crown_ht_base, Remarks) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cur.execute(insert_query, data)
        con.commit()
    except mysql.connector.Error as err:
        st.error(f"Error inserting data: {err}")

# Update existing data
def update_data(con, cur, data, plot_id):
    update_query = """
    UPDATE fradata2024 SET col_no=%s, row_no=%s, plot_number=%s, tree_no=%s, bearing=%s, distance=%s, 
    species_code=%s, species_name=%s, dbh_cm=%s, quality_class=%s, crown_class=%s, 
    sample_type=%s, tree_ht_m=%s, crown_ht_m=%s, tree_ht_base=%s, crown_ht_base=%s, 
    Remarks=%s WHERE plot_id=%s
    """
    try:
        cur.execute(update_query, data + (plot_id,))
        con.commit()
    except mysql.connector.Error as err:
        st.error(f"Error updating data: {err}")

# Delete data
def delete_data(con, cur, plot_id):
    delete_query = "DELETE FROM fradata2024 WHERE plot_id=%s"
    try:
        cur.execute(delete_query, (plot_id,))
        con.commit()
    except mysql.connector.Error as err:
        st.error(f"Error deleting data: {err}")

# Create table if not exists
def create_table(cur):
    query = """
    CREATE TABLE IF NOT EXISTS fradata2024 (
        col_no INT,
        row_no INT,
        plot_number INT,
        plot_id VARCHAR(50) PRIMARY KEY,
        tree_no INT,
        bearing INT,
        distance DECIMAL(4,1),
        species_code INT,
        species_name VARCHAR(50),
        dbh_cm DECIMAL(4,1),
        quality_class INT,
        crown_class INT,
        sample_type INT,
        tree_ht_m DECIMAL(4,1),
        crown_ht_m DECIMAL(4,1),
        tree_ht_base DECIMAL(4,1),
        crown_ht_base DECIMAL(4,1),
        Remarks VARCHAR(100)
    );
    """
    try:
        cur.execute(query)
    except mysql.connector.Error as err:
        st.error(f"Error creating table: {err}")

# Streamlit app
def main():
    st.title("Tree Data Entry Form")

    # Create a connection to the database
    con = create_connection()

    if con is not None:
        cur = con.cursor()
        create_table(cur)

        menu = ["Add New", "Edit", "Delete", "View"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Add New":
            st.subheader("Enter New Tree Data")
            # Input form
            col_no = st.number_input("col: ", step=1)
            row_no = st.number_input("row: ", step=1)
            plot_number = st.number_input("plot_number: ", step=1)
            plot_id = st.text_input("plot_id", key="plot_id_add")
            tree_no = st.number_input("tree_no: ", step=1)
            bearing = st.number_input("bearing: ", step=1)
            distance = st.number_input("distance: ", value=0.0)
            species_code = st.number_input("species_code: ", step=1)
            species_name = st.text_input("species_name: ")
            dbh_cm = st.number_input("dbh_cm: ")
            quality_class = st.number_input("quality_class: ", step=1)
            crown_class = st.number_input("crown_class: ", step=1)
            sample_type = st.number_input("sample_type: ", step=1)
            tree_ht_m = st.number_input("tree_ht_m: ")
            crown_ht_m = st.number_input("crown_ht_m: ")
            tree_ht_base = st.number_input("tree_ht_base: ")
            crown_ht_base = st.number_input("crown_ht_base: ")
            Remarks = st.text_input("Remarks: ")

            if st.button("Add Data"):
                data = (col_no, row_no, plot_number, plot_id, tree_no, bearing, distance, species_code,
                        species_name, dbh_cm, quality_class, crown_class, sample_type, tree_ht_m,
                        crown_ht_m, tree_ht_base, crown_ht_base, Remarks)
                insert_data(con, cur, data)
                st.success("Data added successfully!")

        elif choice == "Edit":
            st.subheader("Update Existing Tree Data")
            plot_id = st.text_input("Enter plot_id to Update: ", key="plot_id_edit")

            if st.button("Fetch Data"):
                cur.execute("SELECT * FROM fradata2024 WHERE plot_id=%s", (plot_id,))
                result = cur.fetchone()

                if result:
                    # Unpack the existing data
                    col_no, row_no, plot_number, existing_plot_id, tree_no, bearing, distance, species_code, \
                    species_name, dbh_cm, quality_class, crown_class, sample_type, tree_ht_m, \
                    crown_ht_m, tree_ht_base, crown_ht_base, Remarks = result

                    # Input fields with existing data
                    col_no = st.number_input("col: ", value=col_no, step=1)
                    row_no = st.number_input("row: ", value=row_no, step=1)
                    plot_number = st.number_input("plot_number: ", value=plot_number, step=1)
                    tree_no = st.number_input("tree_no: ", value=tree_no, step=1)
                    bearing = st.number_input("bearing: ", value=bearing, step=1)
                    distance = st.number_input("distance: ", value=float(distance))
                    species_code = st.number_input("species_code: ", value=species_code, step=1)
                    species_name = st.text_input("species_name: ", value=species_name)
                    dbh_cm = st.number_input("dbh_cm: ", value=float(dbh_cm))
                    quality_class = st.number_input("quality_class: ", value=quality_class, step=1)
                    crown_class = st.number_input("crown_class: ", value=crown_class, step=1)
                    sample_type = st.number_input("sample_type: ", value=sample_type, step=1)
                    tree_ht_m = st.number_input("tree_ht_m: ", value=float(tree_ht_m))
                    crown_ht_m = st.number_input("crown_ht_m: ", value=float(crown_ht_m))
                    tree_ht_base = st.number_input("tree_ht_base: ", value=float(tree_ht_base))
                    crown_ht_base = st.number_input("crown_ht_base: ", value=float(crown_ht_base))
                    Remarks = st.text_input("Remarks: ", value=Remarks)

                    if st.button("Update Data"):
                        new_data = (col_no, row_no, plot_number, tree_no, bearing, distance, species_code,
                                    species_name, dbh_cm, quality_class, crown_class, sample_type,
                                    tree_ht_m, crown_ht_m, tree_ht_base, crown_ht_base, Remarks)
                        update_data(con, cur, new_data, plot_id)
                        st.success(f"Data updated for plot_id: {plot_id}")
                else:
                    st.error(f"No record found for plot_id: {plot_id}")

        elif choice == "Delete":
            st.subheader("Delete Tree Data")
            plot_id = st.text_input("Enter plot_id to Delete: ", key="plot_id_delete")

            if st.button("Delete Data"):
                delete_data(con, cur, plot_id)
                st.success(f"Data deleted for plot_id: {plot_id}")

        elif choice == "View":
            st.subheader("View All Tree Data")
            records = fetch_data(cur)

            if records:
                # Define the column names based on your table structure
                columns = ['col_no', 'row_no', 'plot_number', 'plot_id', 'tree_no', 'bearing', 'distance',
                           'species_code', 'species_name', 'dbh_cm', 'quality_class', 'crown_class',
                           'sample_type', 'tree_ht_m', 'crown_ht_m', 'tree_ht_base', 'crown_ht_base', 'Remarks']

                # Convert the records into a DataFrame
                df = pd.DataFrame(records, columns=columns)

                # Display the DataFrame in a table
                st.dataframe(df)
            else:
                st.write("No records found.")

        # Close cursor and connection
        cur.close()
        con.close()

if __name__ == '__main__':
    main()
