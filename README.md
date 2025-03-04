# CheckPoint 
## team 13

An app designed to ensure trust between couriers and package recipients.

## 🚀 Demo
For a detailed walkthrough, check out our presentation on Canva:  
 **Canva:** [Check it out here](https://www.canva.com/design/DAGgvwtPrMA/q8wfSf0MzZcYXvbUBQ4M3Q/edit?utm_content=DAGgvwtPrMA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
 **PDF:**  [CheckPoint.pdf]()
📽 **Video:**  https://github.com/VoicuTomut/networkx/blob/main/Demovideo.mp4
---

## 📥 Installation
Follow these steps to set up and run CheckPoint:

1. Save your order list as a CSV file named `DataDelivery.csv`.
2. Install all dependencies by running:
   ```bash
   pip install -e .
   ```
3. Start the application:
   ```bash
   python order_system.py
   ```

---

## 📌 How to Use
1. Enter the delivery person's phone number.
2. Press **"Delivery"**.
3. Select the active order (this will generate a QR code).
4. The recipient scans the QR code to receive a verification code.
5. The recipient enters the code, and the order status updates to **"Delivered"**.

---

## 🛠 Technologies
CheckPoint leverages advanced APIs to enhance security and reliability:

- **Location Verification:** Ensures the courier is at the correct location, offering better security than GPS by preventing VPN spoofing.
- **Phone Number Verification:** Confirms deliveries reach the intended recipient.
- **SIM Swap Detection:** Detects if the recipient's SIM card has been changed, reducing fraud risks.

---

🔒 **CheckPoint**—bringing trust and security to deliveries.

