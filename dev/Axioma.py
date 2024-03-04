#import os, pathlib
import ctypes
from ctypes import *
from ctypes import wintypes
from pathlib import Path

LIB_QUIK_API = cdll.LoadLibrary(r"C:\Trans2QuikAPI\trans2quik.dll")

#   C++ signatures

#   long TRANS2QUIK_API __stdcall TRANS2QUIK_CONNECT (
#       LPSTR lpstConnectionParamsString, 
#       long* pnExtendedErrorCode, 
#       LPSTR lpstrErrorMessage, 
#       DWORD dwErrorMessageSize);

#   long TRANS2QUIK_API __stdcall TRANS2QUIK_SEND_ASYNC_TRANSACTION (
#        LPSTR lpstTransactionString, 
#        long* pnExtendedErrorCode, 
#        LPSTR lpstErrorMessage, 
#        DWORD dwErrorMessageSize);

#   connect

PATH_2_QUIK = "C:/BCS_Work/QUIK_BCS/"
PATH_2_QUIK = str(Path(PATH_2_QUIK)) 
PATH_2_QUIK = bytes(PATH_2_QUIK,'ascii')

_TRANS2QUIK_CONNECT = LIB_QUIK_API.TRANS2QUIK_CONNECT
_TRANS2QUIK_CONNECT.restype = c_long
_TRANS2QUIK_CONNECT.argtypes = [wintypes.LPSTR, 
                                ctypes.POINTER(c_long), 
                                wintypes.LPSTR,  
                                wintypes.DWORD]

lpstrPathToQUIK = PATH_2_QUIK
pnExtendedErrorCode = ctypes.c_long()
lpstrErrorMessage = create_string_buffer(250)
dwErrorMessageSize = 250

FunctionResult = _TRANS2QUIK_CONNECT(lpstrPathToQUIK,
                                     ctypes.byref(pnExtendedErrorCode), 
                                     lpstrErrorMessage, 
                                     dwErrorMessageSize)

print()
print("connect:")
print("FunctionResult = ", FunctionResult)
print("ErrorCode =", pnExtendedErrorCode.value)
print("error = ", lpstrErrorMessage.value,"\n")

#   send_async_transaction

_TRANS2QUIK_SEND_ASYNC_TRANSACTION = LIB_QUIK_API.TRANS2QUIK_SEND_ASYNC_TRANSACTION
_TRANS2QUIK_SEND_ASYNC_TRANSACTION.restype = c_long
_TRANS2QUIK_SEND_ASYNC_TRANSACTION.argtypes = [wintypes.LPSTR, 
                                               ctypes.POINTER(c_long), 
                                               wintypes.LPSTR,  
                                               wintypes.DWORD]

#mainString = "Mode=" + nMode + 
#              " TradeNum=" + nNumber + 
#              " OrderNum=" + nOrderNumber +
#              " Class=" + ClassCode +
#              " Sec=" + SecCode +
#              " Price=" + dPrice + 
#              " Volume=" + nQty + 
#              " Value=" + dValue + 
#              " IsSell=" + nIsSell;

#transactionString = b"ACTION=NEW_ORDER; TRANS_ID=888; CLASSCODE=SPBFUT; SECCODE=RIH4; ACCOUNT=A717ykf; CLIENT_CODE=E7; TYPE=L; OPERATION=B; QUANTITY=1; PRICE=109000;"
transactionString = b"ACTION=NEW_ORDER; TRANS_ID=888; CLASSCODE=TQBR; SECCODE=OZON; ACCOUNT=L01-00000F00; CLIENT_CODE=1220166; TYPE=L; OPERATION=B; QUANTITY=200; PRICE=3160 ;"
pnExtendedErrorCode = ctypes.c_long()
lpstrErrorMessage = create_string_buffer(250)
dwErrorMessageSize = 250

FunctionResult = _TRANS2QUIK_SEND_ASYNC_TRANSACTION(transactionString,
                                                    ctypes.byref(pnExtendedErrorCode), 
                                                    lpstrErrorMessage, 
                                                    dwErrorMessageSize)



print("send_async_transaction:")
print("FunctionResult = ", FunctionResult)
print("ErrorCode =", pnExtendedErrorCode.value)
print("error = ", lpstrErrorMessage.value,"\n")




