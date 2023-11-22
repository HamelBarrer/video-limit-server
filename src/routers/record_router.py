from io import BytesIO

import qrcode
from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse

from ..repositories import record_repository

router = APIRouter(
    prefix='/api/v1/record'
)


@router.get('/')
async def get_records():
    records = record_repository.read_record()
    return records


@router.get('/{record_id}')
async def get_record(record_id: int):
    record = record_repository.record(record_id)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(record.location)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    img_byte_array = BytesIO()
    qr_img.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return StreamingResponse(content=img_byte_array, media_type="image/png")


@router.post('/')
async def create_record(record: UploadFile, request: Request):
    try:
        host = request.client.host
        port = request.headers.get('host').split(':')[1]

        with open(f'static/{record.filename}', "wb") as f:
            content = await record.read()
            f.write(content)

        location_file = f'http://{host}:{port}/static/{record.filename}'

        record = record_repository.registered_record(
            record.filename,
            location_file
        )

        return record

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(e)}"})
