from mySolver.Node           import Node2D
from mySolver.Element.Elem2D import CPS3, CPE3, CPS4, CPE4, CPS6, CPE6, CPS8, CPE8, CPS8R, CPE8R, CPS4I, CPE4I
from mySolver.Material       import Material
from mySolver.Section        import ShellSection
from mySolver.Analysis       import AnalysisStatic

class Reader():

    def __init__(self, path):

        self.node_list        = []
        self.material_list    = []
        self.section_list     = []
        self.element_list     = []
        self.constraint_list  = []
        self.load_list        = []

        self.keywords_with_error = []

        with open(path, 'r') as f:
            text = f.readlines()

        lines = []

        for line in text:
            
            line = line.strip().replace(" ", "")
            
            if not (line == "" or line.startswith("**")):
                lines.append(line.upper().split(","))

        self.lines = iter(lines)

        self.next_line()

        self.keyword()

    def export(self):
        return self.analysis

    def keyword(self):

        while True:

            if self.line is None:
                self.EOF()
                return 

            if not self.word[0] == "*":
                print("無効なデータ行です")
                exit()


            if   self.word == "*NODE":
                self.node()

            elif self.word == "*MATERIAL":
                self.material()

            elif self.word == "*SECTION":
                self.section()

            elif self.word == "*ELEMENT":
                self.element()

            elif self.word == "*BOUNDARY":
                self.boundary()

            elif self.word == "*LOAD":
                self.load()

            elif self.word == "*STATIC":
                self.static()

            else:
                print("不明なキーワードです")
                exit()


    def check_params(self, params, required, optional):

        entire = {**required, **optional}
        valid = True

        for required_key in required.keys():

            if not required_key in params.keys():
                print(f"パラメータ<{required_key}>は必須です")
                valid = False

        for key, value in params.items():

            if not key in entire.keys():
                print(f"パラメータ<{key}>は不明なパラメータです")
                valid = False

            else:

                if type(entire[key]) is list: 
                    if not value in entire[key]:
                        print(f"パラメータ<{key}>の値[{value}]は不正です")
                        valid = False
                
                elif entire[key] is int:
                    try:
                        int(value)
                    except ValueError:
                        print(f"パラメータ<{key}>の値[{value}]は不正です")
                        valid = False

        # if valid:
        #     print("パラメータチェック: OK")

        return valid

    def skip_data_line(self):

        print("データ行の読み込みを中止します")

        while True:

            if not self.next_line() or self.word[0] == "*":
                return


    def node(self):

        # print("*NODE")

        params = self.read_params()

        required = {"DIM": ["2D", "3D"]}
        optional = {}

        if not self.check_params(params, required, optional):
            self.keywords_with_error.append("*NODE")

        if len(self.keywords_with_error) > 0:
            self.skip_data_line()
            return


        if   params["DIM"] == "2D":
            dim = 2
        elif params["DIM"] == "3D":
            dim = 3


        data_lines = self.data()

        for data in data_lines:

            try:
                data[0] = int(data[0])

            except ValueError:
                print("IDは整数でなければなりません")
                exit()

            if not len(data) == dim + 1:
                print("座標の数が次元と一致しません")
                exit()

            for i in range(1, dim + 1):

                try:
                    data[i] = float(data[i])

                except ValueError:
                    print("座標は浮動小数点数でなければなりません")
                    exit()

            if   dim == 2:
                self.node_list.append(Node2D(data[0], len(self.node_list), data[1], data[2]))
            elif dim == 3:
                self.node_list.append(Node2D(data[0], len(self.node_list), data[1], data[2], data[3]))


    def material(self):

        # print("*MATERIAL")

        params = self.read_params()

        required = {}
        optional = {}

        if not self.check_params(params, required, optional):
            self.keywords_with_error.append("*MATERIAL")

        if len(self.keywords_with_error) > 0:
            self.skip_data_line()
            return


        data_lines = self.data()

        for data in data_lines:

            try:
                data[0] = int(data[0])

            except ValueError:
                print("IDは整数でなければなりません")
                exit()

            if not len(data) == 3:
                print("与えられた物性値の数が異常です")
                exit()

            for i in range(1, 3):

                try:
                    data[i] = float(data[i])

                except ValueError:
                    print("物性値は浮動小数点数でなければなりません")
                    exit()

            self.material_list.append(Material(data[0], data[1], data[2]))

    def section(self):

        # print("*SECTION")

        params = self.read_params()

        required = {"TYPE": ["SHELL", "SOLID"]}
        optional = {}

        if not self.check_params(params, required, optional):
            self.keywords_with_error.append("*SECTION")

        if len(self.keywords_with_error) > 0:
            self.skip_data_line()
            return


        data_lines = self.data()

        for data in data_lines:

            if params["TYPE"] == "SHELL" and not len(data) == 3:
                print("与えられた数値の数が異常です")
                exit()

            if params["TYPE"] == "SOLID" and not len(data) == 2:
                print("与えられた数値の数が異常です")
                exit()

            try:
                data[0] = int(data[0])

            except ValueError:
                print("IDは整数でなければなりません")
                exit()

            try:
                data[1] = int(data[1])

            except ValueError:
                print("IDは整数でなければなりません")
                exit()

            material = find_entity(self.material_list, data[1])
            
            if material is None:
                print("マテリアルが存在しません")

            if params["TYPE"] == "SHELL":

                try:
                    data[2] = float(data[2])

                except ValueError:
                    print("厚みは浮動小数点数でなければなりません")
                    exit()

            if   params["TYPE"] == "SHELL":
                self.section_list.append(ShellSection(data[0], material, data[2]))
            elif params["TYPE"] == "SOLID":
                self.section_list.append(SolidSection(data[0], material))


    def element(self):
        # print("*ELEMENT")

        params = self.read_params()

        elem_type = ["CPS3", "CPE3", "CPS4", "CPE4", "CPS6", "CPE6", "CPS8", "CPE8", "CPS8R", "CPE8R", "CPS4I", "CPE4I"]

        required = {"TYPE": elem_type , "SECTION": int}
        optional = {}

        if not self.check_params(params, required, optional):
            self.keywords_with_error.append("*ELEMENT")

        if len(self.keywords_with_error) > 0:
            self.skip_data_line()
            return



        section = find_entity(self.section_list, int(params["SECTION"]))
        
        if section is None:
            print("セクションが存在しません")


        data_lines = self.data()

        for data in data_lines:

            if params["TYPE"] in ["CPS3", "CPE3"] and not len(data) == 4:
                print("与えられた数値の数が異常です")
                exit()

            if params["TYPE"] in ["CPS6", "CPE6"] and not len(data) == 7:
                print("与えられた数値の数が異常です")
                exit()

            if params["TYPE"] in ["CPS4", "CPE4", "CPS4I", "CPE4I"] and not len(data) == 5:
                print("与えられた数値の数が異常です")
                exit()

            if params["TYPE"] in ["CPS8", "CPE8", "CPS8R", "CPE8R"] and not len(data) == 9:
                print("与えられた数値の数が異常です")
                exit()

            try:
                data[0] = int(data[0])

            except ValueError:
                print("IDは整数でなければなりません")
                exit()


            try:
                data[1] = int(data[1])

            except ValueError:
                print("IDは整数でなければなりません")
                exit()

            node_list = []

            if params["TYPE"] in ["CPS3", "CPE3"]:
                 
                for i in range(1, 4):

                    try:
                        data[i] = int(data[i])

                    except ValueError:
                        print("IDは整数でなければなりません")
                        exit()

                    node = find_entity(self.node_list, data[i])

                    if node is None:
                        print("ノードが存在しません")
                        exit()

                    node_list.append(node)

                if   params["TYPE"] == "CPS3":
                    self.element_list.append(CPS3(data[0], node_list, section))
                elif params["TYPE"] == "CPE3":
                    self.element_list.append(CPE3(data[0], node_list, section))

            elif params["TYPE"] in ["CPS6", "CPE6"]:
                 
                for i in range(1, 7):

                    try:
                        data[i] = int(data[i])

                    except ValueError:
                        print("IDは整数でなければなりません")
                        exit()

                    node = find_entity(self.node_list, data[i])

                    if node is None:
                        print("ノードが存在しません")
                        exit()

                    node_list.append(node)

                if   params["TYPE"] == "CPS6":
                    self.element_list.append(CPS6(data[0], node_list, section))
                elif params["TYPE"] == "CPE6":
                    self.element_list.append(CPE6(data[0], node_list, section))

            elif params["TYPE"] in ["CPS4", "CPE4", "CPS4I", "CPE4I"]:
                 
                for i in range(1, 5):

                    try:
                        data[i] = int(data[i])

                    except ValueError:
                        print("IDは整数でなければなりません")
                        exit()

                    node = find_entity(self.node_list, data[i])

                    if node is None:
                        print("ノードが存在しません")
                        exit()

                    node_list.append(node)

                if   params["TYPE"] == "CPS4":
                    self.element_list.append(CPS4(data[0], node_list, section))
                elif params["TYPE"] == "CPE4":
                    self.element_list.append(CPE4(data[0], node_list, section))
                elif params["TYPE"] == "CPS4I":
                    self.element_list.append(CPS4I(data[0], node_list, section))
                elif params["TYPE"] == "CPE4I":
                    self.element_list.append(CPE4I(data[0], node_list, section))


            elif params["TYPE"] in ["CPS8", "CPE8", "CPS8R", "CPE8R"]:
                 
                for i in range(1, 9):

                    try:
                        data[i] = int(data[i])

                    except ValueError:
                        print("IDは整数でなければなりません")
                        exit()

                    node = find_entity(self.node_list, data[i])

                    if node is None:
                        print("ノードが存在しません")
                        exit()

                    node_list.append(node)

                if   params["TYPE"] == "CPS8":
                    self.element_list.append(CPS8(data[0], node_list, section))
                elif params["TYPE"] == "CPE8":
                    self.element_list.append(CPE8(data[0], node_list, section))
                elif params["TYPE"] == "CPS8R":
                    self.element_list.append(CPS8R(data[0], node_list, section))
                elif params["TYPE"] == "CPE8R":
                    self.element_list.append(CPE8R(data[0], node_list, section))


    def boundary(self):

        # print("*BOUNDARY")

        params = self.read_params()

        required = {}
        optional = {}

        if not self.check_params(params, required, optional):
            self.keywords_with_error.append("*BOUNDARY")

        if len(self.keywords_with_error) > 0:
            self.skip_data_line()
            return



        data_lines = self.data()

        for data in data_lines:

            if not len(data) == 3:
                print("与えられた数値の数が不正です")
                exit()

            try:
                data[0] = int(data[0])

            except ValueError:
                print("IDは整数でなければなりません")
                exit()

            node = find_entity(self.node_list, data[0])

            if node is None:
                print("ノードが存在しません")
                exit()

            try:
                data[1] = int(data[1])

            except ValueError:
                print("DOFは整数でなければなりません")
                exit()

            if not data[1] in range(1, 7):
                print("DOFは1から6の間でなければなりません")
                exit()

            try:
                 data[2] = float(data[2])
            except ValueError:
                print("変位量は浮動小数点数でなければなりません")
                exit()

            self.constraint_list.append([node, data[1], data[2]])


    def load(self):

        # print("*LOAD")

        params = self.read_params()

        required = {}
        optional = {}

        if not self.check_params(params, required, optional):
            self.keywords_with_error.append("*LOAD")

        if len(self.keywords_with_error) > 0:
            self.skip_data_line()
            return


        data_lines = self.data()

        for data in data_lines:

            if not len(data) == 3:
                print("与えられた数値の数が不正です")
                exit()

            try:
                data[0] = int(data[0])

            except ValueError:
                print("IDは整数でなければなりません")
                exit()

            node = find_entity(self.node_list, data[0])

            if node is None:
                print("ノードが存在しません")
                exit()

            try:
                data[1] = int(data[1])

            except ValueError:
                print("DOFは整数でなければなりません")
                exit()

            if not data[1] in range(1, 7):
                print("DOFは1から6の間でなければなりません")
                exit()

            try:
                 data[2] = float(data[2])
            except ValueError:
                print("荷重値は浮動小数点数でなければなりません")
                exit()

            self.load_list.append([node, data[1], data[2]])

    def static(self):
        
        self.analysis = AnalysisStatic()

        self.analysis.add_nodes(self.node_list)
        self.analysis.add_elems(self.element_list)
        self.analysis.add_constraints(self.constraint_list)
        self.analysis.add_loads(self.load_list)

        self.next_line()


    def read_params(self):

        params = {} 

        while True:

            try:
                self.word = next(self.words)

            except StopIteration:
                return params

            param = self.word.split("=")

            if len(param) > 2:
                print("パラメータの指定が無効です")
                exit()

            if param[0] == "":
                print("パラメータ名がありません")
                exit()

            if param[0] in params:
                print("パラメータが重複しています")
                exit()
            

            if len(param) == 2:
                params[param[0]] = param[1]
            elif len(param) == 1:
                params[param[0]] = ""

    def data(self):

        data_lines = []

        while True:

            if not self.next_line() or self.word[0] == "*":
                return data_lines

            self.words = iter(self.line)

            data = []
            
            while True:

                try:
                    self.word = next(self.words)

                except StopIteration:
                    data_lines.append(data)
                    break

                data.append(self.word)


    def EOF(self):
        pass

    def next_line(self):

        try:
            self.line = next(self.lines)

        except StopIteration:
            self.line = None
            return False
             
        self.words = iter(self.line)
        self.word = next(self.words)

        return True


def find_entity(entity_list, ID):

    for i in range(len(entity_list)):

        entity = entity_list[i]

        if entity_list[i].ID == ID:
            return entity

    return None


