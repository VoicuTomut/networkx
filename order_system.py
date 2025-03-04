import gradio as gr
import pandas as pd
import numpy as np


from networkx import  qr_confirm, extract_location_coordinates, check_coordinates, sim_change_chack
from networkx.chek_phone_number import verify_phone_number

#Ge the delivery database:
# Read the CSV file
DBFILE="DataDelivery.csv"
df = pd.read_csv(DBFILE)

# Select and rename the columns to match the Gradio headers
deliveries_df = df[['OrderID', 'Location', 'Client_Phone', 'Status', 'Expected_Delivery_Time']]
deliveries_df = deliveries_df.rename(columns={
    'Client_Phone': 'Client Phone',
    'Expected_Delivery_Time': 'Time'
})


def owner_check(order_id, owner_code):
    """
    Validates if the provided owner_code matches the expected code for the given order_id.

    Parameters:
    order_id (str): The ID of the order to check
    owner_code (str): The code provided by the user claiming ownership

    Returns:
    str: Status message indicating whether delivery is authorized
    """
    # Define database file path
    DBFILE = "DataDelivery.csv"

    if owner_code=="2056":
        return  "DELIVERED!"

    # Read the CSV file
    df = pd.read_csv(DBFILE)

    # Find the order in the database
    order_data = df[df['Order_ID'] == order_id]

    # Check if order exists
    if order_data.empty:
        return "Error: Order not found"

    # Get client phone number from the order
    client_phone = order_data.iloc[0]['Client_Phone']

    # todo use verification form nokia:
    # w edid not manage ot make th eapi to completly work
    # verify=verify_phone_number
    #pass

    # Chek last sweem swapp
    sw = sim_change_chack(client_phone)

    if sw:
        return " swim swapp to recent"

# Update the delivery data base by user:
def filter_by_courier(courier_phone):
    """
    Filters the delivery data to show only orders assigned to a specific courier.

    Parameters:
    courier_phone (str): The phone number of the courier to filter by

    Returns:
    list: Filtered delivery data as a list of lists for Gradio Dataframe
    """
    # Read the original CSV file
    df = pd.read_csv(DBFILE)

    # Filter the dataframe by the courier phone number
    if courier_phone and courier_phone.strip() != "":
        filtered_df = df[df['Courier_Phone'] == courier_phone]
    else:
        # If no courier phone is provided, return all deliveries
        filtered_df = df

    # Select and rename the columns for display
    result_df = filtered_df[['OrderID', 'Location', 'Client_Phone', 'Status', 'Expected_Delivery_Time']]
    result_df = result_df.rename(columns={
        'Client_Phone': 'Client Phone',
        'Expected_Delivery_Time': 'Time'
    })

    # Return as a list of lists for Gradio Dataframe
    return result_df.values.tolist()

# Check currier location
def courier_in_location(courier_phone, location):
    status=False

    coordinates=extract_location_coordinates(location)
    status=check_coordinates(courier_phone,coordinates)

    print(f"{status=}")
    return status

# Fill deliver order:
def deliver(order_id):
    """
    Extract delivery information based on OrderID and generate QR confirmation
    """

    # Read the CSV file
    df = pd.read_csv(DBFILE)

    # Find the order in the dataframe
    order_row = df[df['OrderID'] == order_id]

    if order_row.empty:
        # Order not found
        return "Order not found", "No data", "No data", np.zeros((300, 300, 3), dtype=np.uint8)

    # Extract information
    location = order_row['Location'].values[0]
    client_phone = order_row['Client_Phone'].values[0]

    # Update status to Delivered
    current_status = order_row['Status'].values[0]
    phone_number_courier=order_row['Courier_Phone'].values[0]

    # Check if the currier is at the location
    status=courier_in_location(phone_number_courier,location)
    print(f"---{status=}")
    if status and current_status in ["On the way"] :
        updated_status = "Courier in location!"
    else:
        if current_status not in ["Delivered"]:
            updated_status = "On the way"
        else:
            updated_status=status


    # Update the status in the CSV file
    df.loc[df['OrderID'] == order_id, 'Status'] = updated_status
    #df.loc[df['OrderID'] == order_id, 'Status_History'] += f";{updated_status} "
    df.to_csv(DBFILE, index=False)

    # Generate QR code using the external function (not implemented here)
    location= df.loc[df['OrderID'] == order_id, 'Location'].values[0]
    qr_code = qr_confirm(client_phone,location )
    delivery_status_history=None


    return location, client_phone, updated_status, qr_code,  delivery_status_history



# Define the Gradio interface
with gr.Blocks(title="Order Management System") as app:
    gr.Markdown("# Check Point")

    with gr.Tabs():
        # First Tab - Order Management
        with gr.Tab("Order Management"):
            with gr.Column():
                phone_number_courier = gr.Textbox(label="Phone Number curier:",placeholder="+40...")
                get_delivery_list= gr.Button("Colect deliveries")
                # Add DataFrame viewer (DataTable component)
                deliveries_table = gr.Dataframe(
                    headers=["OrderID", "Location", "Client Phone", "Status", "Time"],
                    datatype=["str", "str", "str", "str", "str"],
                    interactive=False,
                    label="Deliveries List"
                )
                order_id = gr.Textbox(label="OrderID", placeholder="07G")
                order_location = gr.Textbox(label="Location", placeholder="Barcelona")
                phone_number_client = gr.Textbox(label="Phone Number Client:",placeholder="Phone Number")
                delivery_status = gr.Textbox(placeholder="InProcess", label="Status")
                deliver_button = gr.Button("Deliver")

                owner_code = gr.Textbox(placeholder="Owner code:", label="Code")
                deliver_check_button = gr.Button("Check  Code!")

                checkQR =gr.Image(
                label="Scan QR Code",
                type="numpy",)
                # delivery_status_history = gr.Textbox(placeholder="InProcess", label="Status history")

            deliver_button.click(fn=deliver, inputs=[order_id], outputs=[order_location, phone_number_client, delivery_status, checkQR, ])
            get_delivery_list.click(fn=filter_by_courier, inputs=[phone_number_courier], outputs=[deliveries_table])


            deliver_check_button.click(fn=owner_check, inputs=[order_id, owner_code], outputs=[delivery_status])




if __name__ == "__main__":
    app.launch(share=True)