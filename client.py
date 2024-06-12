import google.generativeai as genai
from enums import GeminiModelEnum
from exceptions import InvalidDataError
from PIL import Image
from io import BytesIO

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"


class GeminiAIClient:
    def __init__(
        self, token, model_name=GeminiModelEnum.GEMINI_PRO.value, chat_history=[]
    ):
        self.chat_history = chat_history
        genai.configure(api_key=token)
        self._genai = genai.GenerativeModel(model_name=model_name)

    async def send_message(self, req):
        if not req.query and not req.image_data:
            raise InvalidDataError

        if req.image_data:
            msg = []
            image = Image.open(BytesIO(req.image_data))
            msg.append(req.query)
            msg.append(image)
            response = self._genai.generate_content(msg)
            response.resolve()
            return response.text
        else:
            chat = self._genai.start_chat(history=self.chat_history)
            response = chat.send_message(req.query)
            self.chat_history = chat.history
            return response.text
