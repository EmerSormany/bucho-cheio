import qrcode
import json
from io import BytesIO
import base64
from PIL import Image
# from pyzbar.pyzbar import decode

class QRCode:
    @staticmethod
    def generate_qr_code(usuario_id, vaga_id):
        dados = {
            "usuario_id": usuario_id,
            "vaga_id": vaga_id
        }
        payload = json.dumps(dados)

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(payload)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return qr_code_base64
