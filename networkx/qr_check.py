import qrcode

import os
from .chek_phone_number import get_client_credentials,generate_authorization,get_confirm_link

#Constants
Credentials=get_client_credentials()
Authorization=generate_authorization()

def link_to_qr(url, output_path="qrcode.png", box_size=10, border=4, fill_color="black", back_color="white"):
    """
    Generates a QR code image from a URL link.

    Parameters:
    -----------
    url : str
        The URL to encode in the QR code
    output_path : str, optional
        Path where the QR code image will be saved (default: "qrcode.png")
    box_size : int, optional
        Size of each box in the QR code (default: 10)
    border : int, optional
        Border size in boxes (default: 4)
    fill_color : str, optional
        Color of the QR code (default: "black")
    back_color : str, optional
        Background color (default: "white")

    Returns:
    --------
    str
        Path to the saved QR code image
    """

    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border
    )

    # Add data to the QR code
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    # Save the image
    img.save(output_path)

    print(f"QR code saved as: {os.path.abspath(output_path)}")
    return output_path


# genrate the confirmatin QR:
def qr_confirm(client_phone ,location ):

    print(f"{client_phone=}: {location=}")

    client_id = Credentials.get("client_id")
    client_secret = Authorization.get("client_secret")

    authorization_endpoint = Authorization.get("authorization_endpoint")
    token_endpoint = Authorization.get("token_endpoint")

    redirect_uri = "https://example.com/redirect"
    login_hint = client_phone

    auth_link = get_confirm_link(
        authorization_endpoint,
        client_id,
        login_hint,
        redirect_uri,
        response_type="code",
        scope="number-verification:verify",
        state="c3VwZXItc2VjcmV0"
    )

    auth_link="https://8d84df437535aaac7d.gradio.live"
    qr=link_to_qr(
        auth_link,
        "check_qr.png",
        box_size=12,
        border=2,
        fill_color="orange",
        back_color="grey"
    )
    return qr


