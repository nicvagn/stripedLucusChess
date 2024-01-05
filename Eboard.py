import ctypes
import os
import time

import LucasCode
import Util



# Install: Wbase #90
# Assign toolbar: Wbase #132


class Eboard:
    def __init__(self):
        self.name = LucasCode.configuration.x_digital_board
        self.driver = None
        self.setup = False
        self.fen_eboard = None
        self.dispatch = None
        self.allowHumanTB = False
        self.working_time = None

    def is_working(self):
        return self.working_time is not None and 1.0 > (time.time() - self.working_time)

    def set_working(self):
        self.working_time = time.time()

    def envia(self, quien, dato):
        # assert LucasCode.prln(quien, dato, self.dispatch)
        return self.dispatch(quien, dato)

    def set_position(self, position):
        # assert LucasCode.prln("set position", position.fen())
        if self.driver:
            if (self.name == "DGT") or (
                    self.name == "Novag UCB" and LucasCode.configuration.x_digital_board_version == 0
            ):
                self.write_position(position.fenDGT())
            else:
                self.write_position(position.fen())

    @staticmethod
    def log(cad):
        import traceback

        with open("dgt.log", "at", encoding="utf-8", errors="ignore") as q:
            q.write("\n[%s] %s\n" % (Util.today(), cad))
            for line in traceback.format_stack():
                q.write("    %s\n" % line.strip())

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

    def activate(self, dispatch):
        # assert LucasCode.prln("activate")
        self.fen_eboard = None
        self.driver = driver = None
        self.side_takeback = None
        self.dispatch = dispatch

        path_eboards = os.path.join(os.getcwd(), "DigitalBoards")
        os.chdir(path_eboards)

        if LucasCode.is_linux:
            functype = ctypes.CFUNCTYPE
            if self.name == "DGT-gon":
                path_so = os.path.join(path_eboards, "libdgt.so")
            elif self.name == "Certabo":
                path_so = os.path.join(path_eboards, "libcer.so")
            elif self.name == "Chessnut":
                path_so = os.path.join(path_eboards, "libnut.so")
            elif self.name == "Pegasus":
                path_so = os.path.join(path_eboards, "libpeg.so")
            elif self.name == "Millennium":
                path_so = os.path.join(path_eboards, "libmcl.so")
            elif self.name == "Citrine":
                path_so = os.path.join(path_eboards, "libcit.so")
            elif self.name == "Saitek":
                path_so = os.path.join(path_eboards, "libosa.so")
            elif self.name == "Square Off":
                path_so = os.path.join(path_eboards, "libsop.so")
            elif self.name == "Tabutronic":
                path_so = os.path.join(path_eboards, "libtab.so")
            else:
                path_so = os.path.join(path_eboards, "libucb.so")
            if os.path.isfile(path_so):
                try:
                    driver = ctypes.CDLL(path_so)
                except:
                    driver = None
                    from LucasCode.QT import QTUtil2

                    if self.name == "Chessnut":
                        QTUtil2.message(
                            None,
                            """It is not possible to install the driver for the board, one way to solve the problem is to install the libraries:
    sudo apt install libqt5pas1
    sudo apt install libhidapi-dev
    or
    sudo dnf install qt5pas-devel
    sudo dnf install hidapi-devel""",
                        )
                    else:
                        QTUtil2.message(
                            None,
                            """It is not possible to install the driver for the board, one way to solve the problem is to install the libraries:
    sudo apt install libqt5pas1
    or
    sudo dnf install qt5pas-devel""",
                        )

        else:
            functype = ctypes.WINFUNCTYPE
            path_eboards = os.path.join(os.getcwd(), "DigitalBoards")

            if self.name == "DGT":
                for path_dll_dgt in (
                        "C:/Program Files (x86)/DGT Projects/",
                        "C:/Program Files (x86)/Common Files/DGT Projects/",
                        "C:/Program Files/DGT Projects/",
                        "C:/Program Files/Common Files/DGT Projects/",
                        "",
                        path_eboards
                ):
                    path_dll = os.path.join(path_dll_dgt, "DGTEBDLL.dll")
                    if os.path.isfile(path_dll):
                        try:
                            driver = ctypes.WinDLL(path_dll)
                        except:
                            pass
            else:
                if self.name == "Certabo":
                    path_dll = os.path.join(path_eboards, "CER_DLL.dll")
                elif self.name == "Chessnut":
                    path_dll = os.path.join(path_eboards, "NUT_DLL.dll")
                elif self.name == "DGT-gon":
                    path_dll = os.path.join(path_eboards, "DGT_DLL.dll")
                elif self.name == "Pegasus":
                    path_dll = os.path.join(path_eboards, "PEG_DLL.dll")
                elif self.name == "Millennium":
                    path_dll = os.path.join(path_eboards, "MCL_DLL.dll")
                elif self.name == "Citrine":
                    path_dll = os.path.join(path_eboards, "CIT_DLL.dll")
                elif self.name == "Saitek":
                    path_dll = os.path.join(path_eboards, "OSA_DLL.dll")
                elif self.name == "Square Off":
                    path_dll = os.path.join(path_eboards, "SOP_DLL.dll")
                elif self.name == "Tabutronic":
                    path_dll = os.path.join(path_eboards, "TAB_DLL.dll")
                else:
                    path_dll = os.path.join(path_eboards, "UCB_DLL.dll")
                if os.path.isfile(path_dll):
                    try:
                        driver = ctypes.WinDLL(path_dll)
                    except:
                        pass

        if driver is None:
            os.chdir(LucasCode.current_dir)
            return False

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

        if self.name != "DGT":
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

    def deactivate(self):
        if self.driver:
            # assert LucasCode.prln("deactivate")
            self.driver._DGTDLL_HideDialog(ctypes.c_int(1))
            if LucasCode.is_windows:
                handle = self.driver._handle
                ctypes.windll.kernel32.FreeLibrary(handle)

            del self.driver
            self.driver = None
            return True
        return False

    def show_dialog(self):
        # assert LucasCode.prln("showdialog")
        if self.driver:
            self.driver._DGTDLL_ShowDialog(ctypes.c_int(1))

    def write_debug(self, activar):
        # assert LucasCode.prln("writeDebug")
        if self.driver:
            self.driver._DGTDLL_WriteDebug(activar)

    def write_position(self, cposicion):
        # assert LucasCode.prln("write_position", cposicion, self.fen_eboard)
        if self.driver and cposicion != self.fen_eboard:
            # log( "Enviado a la DGT" + cposicion )
            self.driver._DGTDLL_WritePosition(cposicion.enLucasCode())
            self.fen_eboard = cposicion
            # self.envia("stableBoard", cposicion.enLucasCode())
            LucasCode.eboard.allowHumanTB = False

    def writeClocks(self, wclock, bclock):
        # assert LucasCode.prln("writeclocks")
        if self.driver:
            if self.name in ("DGT", "DGT-gon"):
                # log( "WriteClocks: W-%s B-%s"%(str(wclock), str(bclock)) )
                self.driver._DGTDLL_SetNRun(wclock.enLucasCode(), bclock.enLucasCode(), 0)

    @staticmethod
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

    @staticmethod
    def dgt2pv(datobyte):
        dato = datobyte.deLucasCode()
        # Coronacion
        if dato[0] in "Pp" and dato[3].lower() != "p":
            return dato[1:3] + dato[4:6] + dato[3].lower()

        return dato[1:3] + dato[4:6]


#    def icon_eboard(self):
#        board = self.name
#        if board == "DGT":
#            return Iconos.DGT()
#        elif board in ("DGT-gon", "Pegasus"):
#            return Iconos.DGTB()
#        elif board == "Certabo":
#            return Iconos.Certabo()
#        elif board == "Chessnut":
#            return Iconos.Chessnut()
#        elif board == "Millennium":
#            return Iconos.Millenium()
#        elif board == "Saitek":
#            return Iconos.Saitek()
#        elif board == "Square Off":
#            return Iconos.SquareOff()
#        elif board == "Tabutronic":
#            return Iconos.Tabutronic()
#        else:
#            return Iconos.Novag()


def version():
    path_version = os.path.join(LucasCode.folder_OS, "DigitalBoards", "version")
    xversion = "0"
    if os.path.isfile(path_version):
        with open(path_version, "rt") as f:
            xversion = f.read().strip()
    return xversion

