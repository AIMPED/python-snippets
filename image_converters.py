from PIL import Image
import numpy as np
import base64
import io


def b64_bytes_to_png_file(b64_bytes: bytes, file_name: str) -> None:
    """
    function stores a *.png- file locally for a given base64- bytestring
    """
    # decode base64- bytestring into bytes object
    bytes_object = base64.decodebytes(b64_bytes)

    # write into buffer
    buffer = io.BytesIO(bytes_object)

    # create and save image locally
    im = Image.open(buffer)
    im.save(file_name)


def png_file_to_b64_bytes(png_file: str, buffer=io.BytesIO()) -> bytes:
    """
    function opens a *.png- file and converts it into a base64- bytestring
    """
    im = Image.open(png_file)

    if im.mode != 'RGBA':
        im = im.convert("RGBA")

    # save image into buffer
    im.save(buffer, format="png")

    # create base64- bytes
    b64_bytes = base64.b64encode(buffer.getvalue())

    return b64_bytes


def image_string_to_b64_bytes(image_string: str) -> bytes:
    """
    function extracts the bytestring (image information)
    from a base64-encoded image string
    """
    # split image string and keep the actual image
    image_data = image_string.split(',')[1]

    # convert into bas64- bytes
    b64_bytes = base64.b64decode(image_data)

    return b64_bytes


def b64_bytes_to_image_string(b64_bytes: bytes) -> str:
    """
    function creates an image string for a given base64- bytestring
    """
    # decode the base64- bytes to utf-8
    decoded = b64_bytes.decode('utf-8')

    # Construct the data URI
    data_uri = f"data:image/png;base64,{decoded}"

    return data_uri


def image_array_to_b64_bytes(array: np.ndarray) -> bytes:
    """
    function converts a numpy array to a base64- bytestring using PIL
    """
    # assure dtype uint8
    array = array.astype(np.uint8)

    # check channels
    channels = array.shape[-1]
    if channels <= 1 or channels > 4:
        raise ValueError(
            f'Number of channels must be 2, 3 or 4. Channels found: {channels}'
        )

    # create a PIL Image
    im = Image.fromarray(array)

    # Convert the PIL Image to a byte stream
    buffer = io.BytesIO()
    im.save(buffer, format='PNG')

    # create base64- bytes
    b64_bytes = base64.b64encode(buffer.getvalue())

    return b64_bytes


def b64_bytes_to_image_array(b64_bytes: bytes) -> np.ndarray:
    """
    function converts a base64- bytestring to a numpy array using PIL
    """
    im = Image.open(
        io.BytesIO(b64_bytes)
    )

    return np.array(im)
