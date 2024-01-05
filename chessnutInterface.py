import ctypes
import os
import time

import LucasCode
import Util
#class chessnut:
#get the path to dir containing drivers
path_eboards = os.path.join(os.getcwd(), "DigitalBoards")
#the path of the object file
path_so = os.path.join(path_eboards, "libnut.so")

def dispatch(data):
    print(data)

class chessnut:
    fen_eboard = None
    driver = driver = None
    side_takeback = None
    dispatch = dispatch



    def dgt2fen(datobyte):
        n = 0
        dato = datobyte.deLucasCode()
        ndato = len(dato)
        caja = [""] * 8
        ncaja = 0
        ntam = 0
        while True:
            if dato[n].isdigit():
                num = int(dato[n])
                if (n + 1 < ndato) and dato[n + 1].isdigit():
                    num = num * 10 + int(dato[n + 1])
                    n += 1
                while num:
                    pte = 8 - ntam
                    if num >= pte:
                        caja[ncaja] += str(pte)
                        ncaja += 1
                        ntam = 0
                        num -= pte
                    else:
                        caja[ncaja] += str(num)
                        ntam += num
                        break

            else:
                caja[ncaja] += dato[n]
                ntam += 1
            if ntam == 8:
                ncaja += 1
                ntam = 0
            n += 1
            if n == ndato:
                break
        if ncaja != 8:
            caja[7] += str(8 - ntam)
        return "/".join(caja)



    '''
    Registers functions for the callbacks from Lucuses functions
    '''
    def activate(self, dispatch):
        # assert LucasCode.prln("activate")
        self.fen_eboard = None
        self.driver = driver = None
        self.side_takeback = None
        self.dispatch = dispatch

        path_eboards = os.path.join(os.getcwd(), "DigitalBoards")
        os.chdir(path_eboards)

        # only for the chessnut rn
        path_so = os.path.join(path_eboards, "libnut.so")

        driver = ctypes.CDLL(path_so)

        functype = ctypes.CFUNCTYPE
        cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)

        cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
        st = cmpfunc(self.registerStatusFunc)
        driver._DGTDLL_RegisterStatusFunc.argtype = [st]
        driver._DGTDLL_RegisterStatusFunc.restype = ctypes.c_int
        driver._DGTDLL_RegisterStatusFunc(st)

        cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
        st = cmpfunc(self.registerScanFunc)
        driver._DGTDLL_RegisterScanFunc.argtype = [st]
        driver._DGTDLL_RegisterScanFunc.restype = ctypes.c_int
        driver._DGTDLL_RegisterScanFunc(st)

        cmpfunc = functype(ctypes.c_int)
        st = cmpfunc(self.registerStartSetupFunc)
        driver._DGTDLL_RegisterStartSetupFunc.argtype = [st]
        driver._DGTDLL_RegisterStartSetupFunc.restype = ctypes.c_int
        driver._DGTDLL_RegisterStartSetupFunc(st)

        cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
        st = cmpfunc(self.registerStableBoardFunc)
        driver._DGTDLL_RegisterStableBoardFunc.argtype = [st]
        driver._DGTDLL_RegisterStableBoardFunc.restype = ctypes.c_int
        driver._DGTDLL_RegisterStableBoardFunc(st)

        cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
        st = cmpfunc(self.registerStopSetupWTMFunc)
        driver._DGTDLL_RegisterStopSetupWTMFunc.argtype = [st]
        driver._DGTDLL_RegisterStopSetupWTMFunc.restype = ctypes.c_int
        driver._DGTDLL_RegisterStopSetupWTMFunc(st)

        cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
        st = cmpfunc(self.registerStopSetupBTMFunc)
        driver._DGTDLL_RegisterStopSetupBTMFunc.argtype = [st]
        driver._DGTDLL_RegisterStopSetupBTMFunc.restype = ctypes.c_int
        driver._DGTDLL_RegisterStopSetupBTMFunc(st)

        cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
        st = cmpfunc(self.registerWhiteMoveInputFunc)
        driver._DGTDLL_RegisterWhiteMoveInputFunc.argtype = [st]
        driver._DGTDLL_RegisterWhiteMoveInputFunc.restype = ctypes.c_int
        driver._DGTDLL_RegisterWhiteMoveInputFunc(st)

        cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
        st = cmpfunc(self.registerBlackMoveInputFunc)
        driver._DGTDLL_RegisterBlackMoveInputFunc.argtype = [st]
        driver._DGTDLL_RegisterBlackMoveInputFunc.restype = ctypes.c_int
        driver._DGTDLL_RegisterBlackMoveInputFunc(st)

        driver._DGTDLL_WritePosition.argtype = [ctypes.c_char_p]
        driver._DGTDLL_WritePosition.restype = ctypes.c_int

        driver._DGTDLL_ShowDialog.argtype = [ctypes.c_int]
        driver._DGTDLL_ShowDialog.restype = ctypes.c_int

        driver._DGTDLL_HideDialog.argtype = [ctypes.c_int]
        driver._DGTDLL_HideDialog.restype = ctypes.c_int

        driver._DGTDLL_WriteDebug.argtype = [ctypes.c_bool]
        driver._DGTDLL_WriteDebug.restype = ctypes.c_int

        driver._DGTDLL_SetNRun.argtype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        driver._DGTDLL_SetNRun.restype = ctypes.c_int

        
        driver._DGTDLL_GetVersion.argtype = []
        driver._DGTDLL_GetVersion.restype = ctypes.c_int
        LucasCode.configuration.x_digital_board_version = driver._DGTDLL_GetVersion()
        try:
            driver._DGTDLL_AllowTakebacks.argtype = [ctypes.c_bool]
            driver._DGTDLL_AllowTakebacks.restype = ctypes.c_int
            driver._DGTDLL_AllowTakebacks(ctypes.c_bool(True))
            cmpfunc = functype(ctypes.c_int)
            st = cmpfunc(self.registerWhiteTakeBackFunc)
            driver._DGTDLL_RegisterWhiteTakebackFunc.argtype = [st]
            driver._DGTDLL_RegisterWhiteTakebackFunc.restype = ctypes.c_int
            driver._DGTDLL_RegisterWhiteTakebackFunc(st)
            cmpfunc = functype(ctypes.c_int)
            st = cmpfunc(self.registerBlackTakeBackFunc)
            driver._DGTDLL_RegisterBlackTakebackFunc.argtype = [st]
            driver._DGTDLL_RegisterBlackTakebackFunc.restype = ctypes.c_int
            driver._DGTDLL_RegisterBlackTakebackFunc(st)
        except:
            pass

        driver._DGTDLL_ShowDialog(ctypes.c_int(1))

        os.chdir(LucasCode.current_dir)
        self.driver = driver
        return True
    

    def registerStatusFunc(self, dato):
        # assert LucasCode.prln("registerStatusFunc", dato)
        self.envia("status", dato)
        return 1

    def registerScanFunc(self, dato):
        # assert LucasCode.prln("registerScanFunc", dato)
        self.envia("scan", self.dgt2fen(dato))
        return 1

    def registerStartSetupFunc(self):
        # assert LucasCode.prln("registerStartSetupFunc")
        self.setup = True
        return 1

    def registerStableBoardFunc(self, dato):
        # assert LucasCode.prln("registerStableBoardFunc", dato)
        self.fen_eboard = self.dgt2fen(dato)
        if self.setup:
            self.envia("stableBoard", self.fen_eboard)
        return 1

    def registerStopSetupWTMFunc(self, dato):
        # assert LucasCode.prln("registerStopSetupWTMFunc", dato)
        if self.setup:
            self.envia("stopSetupWTM", self.dgt2fen(dato))
            self.setup = False
        return 1

    def registerStopSetupBTMFunc(self, dato):
        # assert LucasCode.prln("registerStopSetupBTMFunc", dato)
        if self.setup:
            self.envia("stopSetupBTM", self.dgt2fen(dato))
            self.setup = False
        return 1

    def registerWhiteMoveInputFunc(self, dato):
        # assert LucasCode.prln("registerWhiteMoveInputFunc", dato)
        return self.envia("whiteMove", self.dgt2pv(dato))

    def registerBlackMoveInputFunc(self, dato):
        # assert LucasCode.prln("registerBlackMoveInputFunc", dato)
        return self.envia("blackMove", self.dgt2pv(dato))

    def registerWhiteTakeBackFunc(self):
        # assert LucasCode.prln("registerWhiteTakeBackFunc")
        return self.envia("whiteTakeBack", True)

    def registerBlackTakeBackFunc(self):
        # assert LucasCode.prln("registerBlackTakeBackFunc")
        return self.envia("blackTakeBack", True)




chessnut.activate(dispatch=dispatch)