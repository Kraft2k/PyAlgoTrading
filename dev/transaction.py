import ctypes
from ctypes import *
from ctypes import wintypes
from pathlib import Path



class Trans2Quik:

    LIB_QUIK_API = cdll.LoadLibrary(r"C:\Trans2QuikAPI\trans2quik.dll")

    PATH_2_QUIK = "C:/BCS_Shturm/QUIK_BCS/"
    PATH_2_QUIK = str(Path(PATH_2_QUIK)) 
    PATH_2_QUIK = bytes(PATH_2_QUIK,'ascii')

    _TRANS2QUIK_CONNECT = LIB_QUIK_API.TRANS2QUIK_CONNECT
    _TRANS2QUIK_CONNECT.restype = c_long
    _TRANS2QUIK_CONNECT.argtypes = [wintypes.LPSTR, 
                                    ctypes.POINTER(c_long), 
                                    wintypes.LPSTR,  
                                    wintypes.DWORD]


    _TRANS2QUIK_SEND_ASYNC_TRANSACTION = LIB_QUIK_API.TRANS2QUIK_SEND_ASYNC_TRANSACTION
    _TRANS2QUIK_SEND_ASYNC_TRANSACTION.restype = c_long
    _TRANS2QUIK_SEND_ASYNC_TRANSACTION.argtypes = [wintypes.LPSTR, 
                                                    ctypes.POINTER(c_long), 
                                                    wintypes.LPSTR,  
                                                    wintypes.DWORD]


class TransactionUnit:
    
    def __init__(self, ticker, client_code, operation, quantity, price):

        self.lpstrPathToQUIK = Trans2Quik.PATH_2_QUIK
        self.pnExtendedErrorCode = ctypes.c_long()
        self.lpstrErrorMessage = create_string_buffer(250)
        self.dwErrorMessageSize = 250
        # transaction_string = b"ACTION=NEW_ORDER; TRANS_ID=888; CLASSCODE=TQBR; SECCODE=SIBN; ACCOUNT=L01-00000F00; CLIENT_CODE=2007693; TYPE=L; OPERATION=B; QUANTITY=25; PRICE=825;"
        self.transaction_string = "ACTION=NEW_ORDER; TRANS_ID=888; CLASSCODE=TQBR; "
        seccode_string = "SECCODE=" + str(ticker) + "; "
        self.transaction_string = self.transaction_string + seccode_string
        account_string = "ACCOUNT=L01-00000F00; " # for bcs broker
        client_code_string = "CLIENT_CODE=" + str(client_code)+"; "
        self.transaction_string = self.transaction_string + account_string + client_code_string
        type_string = "TYPE=L; "
        operation_string =  "OPERATION=" + str(operation) + "; "
        self.transaction_string = self.transaction_string + type_string + operation_string
        quantity_string = "QUANTITY=" + str(quantity) + "; "
        price_string = "PRICE=" + str(price) + "; "
        self.transaction_string = self.transaction_string + quantity_string + price_string
        


    

    def quik_api_connect(self):

        FunctionResult = Trans2Quik._TRANS2QUIK_CONNECT(self.lpstrPathToQUIK,
                                     ctypes.byref(self.pnExtendedErrorCode), 
                                     self.lpstrErrorMessage, 
                                     self.dwErrorMessageSize)

        print()
        print("connect:")
        print("FunctionResult = ", FunctionResult)
        print("ErrorCode =", self.pnExtendedErrorCode.value)
        print("error = ", self.lpstrErrorMessage.value,"\n")


    def quik_api_send_async_transction(self):

        print(self.transaction_string)

        FunctionResult = Trans2Quik._TRANS2QUIK_SEND_ASYNC_TRANSACTION(bytes(self.transaction_string,'ascii'),
                                                    ctypes.byref(self.pnExtendedErrorCode), 
                                                    self.lpstrErrorMessage, 
                                                    self.dwErrorMessageSize)

        print("send_async_transaction:")
        print("FunctionResult = ", FunctionResult)
        print("ErrorCode =", self.pnExtendedErrorCode.value)
        print("error = ", self.lpstrErrorMessage.value,"\n")


if __name__ == '__main__':

    portfolio = TransactionUnit("SIBN", "2007693", "B", 25, 825 )
    portfolio.quik_api_connect()
    portfolio.quik_api_send_async_transction()
  