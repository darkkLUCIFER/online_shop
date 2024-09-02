import os

from kavenegar import KavenegarAPI, APIException, HTTPException


class KavenegarService:
    """
        handle sending a different type of sms send it to users
    """
    __instance = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = KavenegarService()
        return cls.__instance

    def send_otp_code(self, phone_number, otp_code):
        """
            send otp code to users
        """
        try:
            api = KavenegarAPI(os.getenv('KAVE_NEGAR_API_KEY'))
            params = {
                'sender': '',  # optional
                'receptor': phone_number,  # multiple mobile number, split by comma
                'message': f'کد تایید شما: {otp_code}',
            }
            response = api.sms_send(params)
            print(response)
        except APIException as e:
            print(e)
        except HTTPException as e:
            print(e)
