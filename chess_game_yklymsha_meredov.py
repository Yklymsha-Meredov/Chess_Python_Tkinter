import tkinter as tk

x = 800
y = 800
win = tk.Tk()
win.title('Chess')
win.geometry(f'{x}x{y}')

win.rowconfigure(0, minsize=y)
win.columnconfigure(0, minsize=x)
c = 0

class Board(tk.Frame):

    def __init__(self):
        super().__init__(master=win)
        for i in range(8):
            self.rowconfigure(i, minsize=y/8)
            self.columnconfigure(i, minsize=x/8)
        self.grid(row=0, column=0, sticky='news')
        self.selected = None
        self.order = 'white'
        self.is_end = ''
        self.tr = ''

    def draw_squares(self):
        for row, row_lst in data_squares.items():
            for column, square in row_lst.items():
                frm = tk.Frame(self, bg=square.color)
                frm.rowconfigure(0, minsize=y/8)
                frm.columnconfigure(0, minsize=x/8)
                frm.grid(row=row_router[row], column=column_router[column], sticky='news')
                widget_squares[row][column] = frm

    def draw_pieces(self):
        for row, row_lst in widget_squares.items():
            for column, square in row_lst.items():
                    for i in square.winfo_children():
                        i.destroy()

        for row, row_lst in data_pieces.items():
            for column, piece in row_lst.items():
                bd = 0 if piece.typ == ' ' else 3
                fg = 'white' if piece.color == 'black' else 'black'
                btn = tk.Button(widget_squares[row][column], bg=piece.act_color(), width=int(x/128), height=int(y/256),
                                bd=bd, fg=fg, font=('Arial', 10), activebackground='green', text=piece.typ)
                btn.configure(command=lambda row=row, column=column: self.move_0(data_pieces[row][column]))
                btn.grid(row=0, column=0)
                widget_pieces[row][column] = btn

    def move_0(self, piece):
        if not self.is_end:
            tempclr = piece.act_color()
            if self.selected and piece.tempclr in clrs:
                for row, row_lst in data_pieces.items():
                    for column, piece_ in row_lst.items():
                        piece_.set_tempclr(None)
                        if piece_.en_passant:
                            piece_.en_passant = False
                if self.selected.typ == 'P':
                    if piece.typ == ' ' and self.selected.column != piece.column:
                        self.en_passant(piece)
                    elif row_router[piece.row] == row_router[self.selected.row] + 2:
                        for row, row_lst in data_pieces.items():
                            if row_router[self.selected.row] + 1 == row_router[row]:
                                for column, piece_ in row_lst.items():
                                    if column == piece.column:
                                        piece_.enpassant()
                        self.move_1(piece)
                    elif row_router[piece.row] == row_router[self.selected.row] - 2:
                        for row, row_lst in data_pieces.items():
                            if row_router[self.selected.row] - 1 == row_router[row]:
                                for column, piece_ in row_lst.items():
                                    if column == piece.column:
                                        piece_.enpassant()
                        self.move_1(piece)
                    elif piece.row in '18':
                        self.pawn_transform(piece)
                    else:
                        self.move_1(piece)
                elif self.selected.typ == 'K' and tempclr == 'magenta':
                    self.castle(piece)
                else:
                    self.move_1(piece)
                self.selected.hasmoved()
                self.selected = None
                self.order = 'black' if self.order == 'white' else 'white'
                self.draw_pieces()
                moves.calc_moves()

            elif piece.typ != ' ':
                for row, row_lst in data_pieces.items():
                    for column, piece_ in row_lst.items():
                        piece_.set_tempclr(None)
                if piece.color == self.order:
                    emove_set = moves.calc_moves()
                    if not emove_set:
                        return None
                    move_set = []
                    for move in emove_set:
                        if move.piece_0 == piece:
                            move_set.append(move)
                    for move in move_set:
                        data_pieces[move.piece_1.row][move.piece_1.column].set_tempclr(move.color)
                self.draw_pieces()
                self.selected = piece

            else:
                for row, row_lst in data_pieces.items():
                    for column, piece in row_lst.items():
                        piece.set_tempclr(None)
                self.selected = None
                self.draw_pieces()
        else:
            self.end(self.is_end)

    def move_1(self, piece):
        data_pieces[piece.row][piece.column] = self.selected
        data_pieces[self.selected.row][self.selected.column] = Piece()
        data_pieces[self.selected.row][self.selected.column].neo()
        data_pieces[piece.row][piece.column].coor()

    def pawn_transform(self, piece):
        self.tr = ''
        self.sel = self.selected
        pawn_tr = tk.Toplevel()
        pawn_tr.title('Pawn transformation')
        var = tk.StringVar(pawn_tr)
        var.set(None)
        def tr_():
            self.tr = var.get()
            test()
            pawn_tr.destroy()
            self.draw_pieces()
            return

        tk.Radiobutton(pawn_tr, text='Q', variable=var, value='Q').pack()
        tk.Radiobutton(pawn_tr, text='R', variable=var, value='R').pack()
        tk.Radiobutton(pawn_tr, text='B', variable=var, value='B').pack()
        tk.Radiobutton(pawn_tr, text='N', variable=var, value='N').pack()
        tk.Button(pawn_tr, text='Confirm', command=tr_).pack()
        
        def test():
            data_pieces[piece.row][piece.column] = self.sel
            data_pieces[piece.row][piece.column].set_color_typ(self.sel.color, self.tr)
            data_pieces[self.sel.row][self.sel.column] = Piece()
            data_pieces[self.sel.row][self.sel.column].neo()
            data_pieces[piece.row][piece.column].coor()

    def en_passant(self, piece):
        for row, row_lst in data_pieces.items():
            if row == self.selected.row:
                for column, piece_ in row_lst.items():
                    if column == piece.column:
                        data_pieces[row][column] = Piece()
                        data_pieces[row][column].neo()
        data_pieces[piece.row][piece.column] = self.selected
        data_pieces[self.selected.row][self.selected.column] = Piece()
        data_pieces[self.selected.row][self.selected.column].neo()
        data_pieces[piece.row][piece.column].coor()
    
    def castle(self, piece):
        if piece.column == 'G':
            data_pieces[self.selected.row]['F'] = data_pieces[self.selected.row]['H']
            data_pieces[self.selected.row]['H'] = Piece()
            data_pieces[self.selected.row]['H'].neo()
            data_pieces[self.selected.row]['F'].coor()
        elif piece.column == 'C':
            data_pieces[self.selected.row]['D'] = data_pieces[self.selected.row]['A']
            data_pieces[self.selected.row]['A'] = Piece()
            data_pieces[self.selected.row]['A'].neo()
            data_pieces[self.selected.row]['D'].coor()
        data_pieces[piece.row][piece.column] = self.selected
        data_pieces[self.selected.row][self.selected.column] = Piece()
        data_pieces[self.selected.row][self.selected.column].neo()
        data_pieces[piece.row][piece.column].coor()

    def end(self, color):
        self.is_end = color
        text = ''
        pad = 0
        if color == 'white' or color == 'black':
            title = 'Checkmate'
            pad = 30
            if color == 'black':
                text = 'White win!'
            elif color == 'white':
                text = 'Black win!'
        elif color == ' ':
            title = 'Stalemate'
            text = 'Draw!'
            pad = 80
        pawn_tr = tk.Toplevel()
        pawn_tr.title(title)
        tk.Label(pawn_tr, text=text, font=('Arial', 30), padx=pad).pack()

board = Board()

class Square():

    def __init__(self):
        self.row = None
        self.column = None
        self.color = None
        self.piece = None
        self.id = None

    def coor(self):
        for row, row_lst in data_squares.items():
            for column, square in row_lst.items():
                if self == square:
                    self.row = row
                    self.column = column

    def set_color(self, color):
        self.color = color

    def set_piece(self, piece):
        self.piece = piece

    def set_id(self, id):
        self.id = id

class Piece():

    def __init__(self):
        self.has_moved = False
        self.en_passant = False
        self.tempclr = None
        self.row = None
        self.column = None
        self.color = None
        self.typ = None
        self.square = None
        self.id = None

    def coor(self):
        for row, row_lst in data_pieces.items():
            for column, piece in row_lst.items():
                if self == piece:
                    self.row = row
                    self.column = column

    def sim_coor(self):
        for row, row_lst in sim_data_pieces.items():
            for column, piece in row_lst.items():
                if self == piece:
                    self.row = row
                    self.column = column

    def set_color_typ(self, color, typ):
        self.color = color
        self.typ = typ

    def set_square(self, square):
        self.square = square

    def hasmoved(self):
        self.has_moved = True

    def set_id(self, id):
        self.id = id

    def set_tempclr(self, color):
        self.tempclr = color

    def act_color(self):
        if self.tempclr == None:
            return self.color
        return self.tempclr
    
    def neo(self):
        global c
        self.coor()
        self.set_square(data_squares[self.row][self.column])
        self.set_color_typ(self.square.color, ' ')
        self.set_id(c)
        c+=1

    def enpassant(self):
        self.en_passant = True

class Move():

    def __init__(self, piece_0, piece_1):
        self.piece_0 = piece_0
        self.piece_1 = piece_1

    def __str__(self):
        return f'{self.piece_0.row}{self.piece_0.column} {self.piece_1.row}{self.piece_1.column} {self.color}'
    
    def set_color(self, color):
        self.color  = color
    
    def set_limit(self, direc, dist):
        self.direc = direc
        self.dist = dist

    def set_direc(self):
        direc = ''
        if row_router[self.piece_1.row] == row_router[self.piece_0.row]:
            pass
        elif row_router[self.piece_1.row] < row_router[self.piece_0.row]:
            direc += 'N'
        elif row_router[self.piece_1.row] > row_router[self.piece_0.row]:
            direc += 'S'
        if column_router[self.piece_1.column] == column_router[self.piece_0.column]:
            pass
        elif column_router[self.piece_1.column] < column_router[self.piece_0.column]:
            direc += 'W'
        elif column_router[self.piece_1.column] > column_router[self.piece_0.column]:
            direc += 'E'
        return direc

class Move_set():

    def __init__(self):
        pass

    def calc_moves(self):
        self.move_set = []
        for row, row_lst in data_pieces.items():
            for column, piece in row_lst.items():
                self.calc_piece(piece)
        
        end_ = True
        for move in self.move_set:
            if move.piece_0.color == board.order:
                end_ = False

        if end_:
            if moves.simulate(None, board.order):
                board.end(board.order)
            else:
                board.end(' ')
        
        return self.move_set

    def calc_piece(self, piece):
        temp_move_set = []
        N = 0
        S = 0
        W = 0
        E = 0
        NW = 0
        NE = 0
        SW = 0
        SE = 0
        direc_router  = {
            'N': N,
            'S': S,
            'W': W,
            'E': E,
            'NW': NW,
            'NE': NE,
            'SW': SW,
            'SE': SE
        }

        if piece.typ == 'K':
            for i in range(8):
                for row, row_lst in data_pieces.items():
                    if row_router[row] == row_router[piece.row] or row_router[row] == row_router[piece.row] + i or row_router[row] == row_router[piece.row] - i:
                        for column, piece_ in row_lst.items():
                            if column_router[column] == column_router[piece.column] or column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                if piece_ != piece:
                                    move = Move(piece, piece_)
                                    move.set_limit(move.set_direc(), i)
                                    if piece_.color != piece.color:
                                        if piece_.typ == ' ':
                                            color = 'green'
                                        else:
                                            color = 'red'
                                        if not direc_router[move.direc]:
                                            direc_router[move.direc] = 1
                                        move.set_color(color)
                                        temp_move_set.append(move)
                                    elif piece_.color == piece.color:
                                        if not direc_router[move.direc]:
                                            direc_router[move.direc] = 1
            
            if not piece.has_moved:
                for row in ['1', '8']:
                    if data_pieces[row]['H'].typ == 'R' and not data_pieces[row]['H'].has_moved:
                        if data_pieces[row]['F'].typ == ' ' and data_pieces[row]['G'].typ == ' ':
                            move = Move(piece, data_pieces[row]['G'])
                            move.set_limit(move.set_direc(), 2)
                            if not direc_router[move.direc]:
                                direc_router[move.direc] = 2
                            color = 'magenta'
                            move.set_color(color)
                            temp_move_set.append(move)
                    if data_pieces[row]['A'].typ == 'R' and not data_pieces[row]['A'].has_moved:
                        if data_pieces[row]['D'].typ == ' ' and data_pieces[row]['C'].typ == ' ' and data_pieces[row]['B'].typ == ' ':
                            move = Move(piece, data_pieces[row]['C'])
                            move.set_limit(move.set_direc(), 3)
                            if not direc_router[move.direc]:
                                direc_router[move.direc] = 3
                            color = 'magenta'
                            move.set_color(color)
                            temp_move_set.append(move)

        if piece.typ == 'Q':
            for i in range(8):
                for row, row_lst in data_pieces.items():
                    if row_router[row] == row_router[piece.row] or row_router[row] == row_router[piece.row] + i or row_router[row] == row_router[piece.row] - i:
                        for column, piece_ in row_lst.items():
                            if column_router[column] == column_router[piece.column] or column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                if piece_ != piece:
                                    move = Move(piece, piece_)
                                    move.set_limit(move.set_direc(), i)
                                    if piece_.color != piece.color:
                                        if piece_.typ == ' ':
                                            color = 'green'
                                        else:
                                            color = 'red'
                                            if not direc_router[move.direc]:
                                                direc_router[move.direc] = i
                                        move.set_color(color)
                                        temp_move_set.append(move)
                                    elif piece_.color == piece.color:
                                        if not direc_router[move.direc]:
                                            direc_router[move.direc] = i

        if piece.typ == 'R':
            for i in range(8):
                for row, row_lst in data_pieces.items():
                    if row_router[row] == row_router[piece.row] or row_router[row] == row_router[piece.row] + i or row_router[row] == row_router[piece.row] - i:
                        for column, piece_ in row_lst.items():
                            if column_router[column] == column_router[piece.column] or column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                if column == piece.column or row == piece.row:
                                    if piece_ != piece:
                                        move = Move(piece, piece_)
                                        move.set_limit(move.set_direc(), i)
                                        if piece_.color != piece.color:
                                            if piece_.typ == ' ':
                                                color = 'green'
                                            else:
                                                color = 'red'
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = i
                                            move.set_color(color)
                                            temp_move_set.append(move)
                                        elif piece_.color == piece.color:
                                            if not direc_router[move.direc]:
                                                direc_router[move.direc] = i

        if piece.typ == 'B':
            for i in range(8):
                for row, row_lst in data_pieces.items():
                    if row_router[row] == row_router[piece.row] or row_router[row] == row_router[piece.row] + i or row_router[row] == row_router[piece.row] - i:
                        for column, piece_ in row_lst.items():
                            if column_router[column] == column_router[piece.column] or column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                if column != piece.column and row != piece.row:
                                    if piece_ != piece:
                                        move = Move(piece, piece_)
                                        move.set_limit(move.set_direc(), i)
                                        if piece_.color != piece.color:
                                            if piece_.typ == ' ':
                                                color = 'green'
                                            else:
                                                color = 'red'
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = i
                                            move.set_color(color)
                                            temp_move_set.append(move)
                                        elif piece_.color == piece.color:
                                            if not direc_router[move.direc]:
                                                direc_router[move.direc] = i

        if piece.typ == 'N':
            knight_lst = [(2, 1), (1, 2)]
            for a, b in knight_lst:
                for row, row_lst in data_pieces.items():
                    if row_router[row] == row_router[piece.row] + a or row_router[row] == row_router[piece.row] - a:
                        for column, piece_ in row_lst.items():
                            if column_router[column] == column_router[piece.column] + b or column_router[column] == column_router[piece.column] - b:
                                if piece_ != piece:
                                    move = Move(piece, piece_)
                                    move.set_limit(move.set_direc(), 2)
                                    if piece_.color != piece.color:
                                        if piece_.typ == ' ':
                                            color = 'green'
                                        else:
                                            color = 'red'
                                        if not direc_router[move.direc]:
                                            direc_router[move.direc] = 2
                                        move.set_color(color)
                                        temp_move_set.append(move)
                                    elif piece_.color == piece.color:
                                        if not direc_router[move.direc]:
                                            direc_router[move.direc] = 2

        if piece.typ == 'P':
            if piece.has_moved:
                x=1
            else:
                x=2
            if piece.color == 'white':
                for i in range(8):
                    for row, row_lst in data_pieces.items():
                        if row_router[row] == row_router[piece.row] - i:
                            for column, piece_ in row_lst.items():
                                if column_router[column] == column_router[piece.column]:
                                    if piece_ != piece:
                                        move = Move(piece, piece_)
                                        move.set_limit(move.set_direc(), i)
                                        if piece_.color != piece.color:
                                            if piece_.typ == ' ':
                                                color = 'green'
                                                move.set_color(color)
                                                if piece_.row == '8':
                                                    move.set_color('magenta')
                                                temp_move_set.append(move)
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = x
                                            else:
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 1
                                        elif piece_.color == piece.color:
                                            if not direc_router[move.direc]:
                                                direc_router[move.direc] = 1
                for i in range(8):
                    for row, row_lst in data_pieces.items():
                        if row_router[row] == row_router[piece.row] - i:
                            for column, piece_ in row_lst.items():
                                if column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                    if piece_ != piece:
                                        move = Move(piece, piece_)
                                        move.set_limit(move.set_direc(), i)
                                        if piece_.color != piece.color:
                                            if piece_.typ != ' ':
                                                color = 'red'
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 1
                                                move.set_color(color)
                                                if piece_.row == '8':
                                                    move.set_color('magenta')
                                                temp_move_set.append(move)
                                            elif piece_.en_passant:
                                                color = 'magenta'
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 1
                                                move.set_color(color)
                                                temp_move_set.append(move)
                                        elif piece_.color == piece.color:
                                            if not direc_router[move.direc]:
                                                direc_router[move.direc] = 1
                
            elif piece.color == 'black':
                for i in range(8):
                    for row, row_lst in data_pieces.items():
                        if row_router[row] == row_router[piece.row] + i:
                            for column, piece_ in row_lst.items():
                                if column_router[column] == column_router[piece.column]:
                                    if piece_ != piece:
                                        move = Move(piece, piece_)
                                        move.set_limit(move.set_direc(), i)
                                        if piece_.color != piece.color:
                                            if piece_.typ == ' ':
                                                color = 'green'
                                                move.set_color(color)
                                                if piece_.row == '1':
                                                    move.set_color('magenta')
                                                temp_move_set.append(move)
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = x
                                            else:
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 1
                                        elif piece_.color == piece.color:
                                            if not direc_router[move.direc]:
                                                direc_router[move.direc] = 1
                for i in range(8):
                    for row, row_lst in data_pieces.items():
                        if row_router[row] == row_router[piece.row] + i:
                            for column, piece_ in row_lst.items():
                                if column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                    if piece_ != piece:
                                        move = Move(piece, piece_)
                                        move.set_limit(move.set_direc(), i)
                                        if piece_.color != piece.color:
                                            if piece_.typ != ' ':
                                                color = 'red'
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 1
                                                move.set_color(color)
                                                if piece_.row == '1':
                                                    move.set_color('magenta')
                                                temp_move_set.append(move)
                                            elif piece_.en_passant:
                                                color = 'magenta'
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 1
                                                move.set_color(color)
                                                temp_move_set.append(move)
                                        elif piece_.color == piece.color:
                                            if not direc_router[move.direc]:
                                                direc_router[move.direc] = 1

        delete_set = []
        for move in temp_move_set:
            limit = direc_router[move.direc]
            if move.piece_0.typ == 'K' and move.color == 'magenta':
                pass
            elif limit:
                if move.dist > limit:
                    delete_set.append(move)

        for move in delete_set:
            temp_move_set.remove(move)

        delete_set = []

        for move in temp_move_set:
            sh_del = False
            if self.simulate(move, move.piece_0.color):
                sh_del = True
            if move.piece_0.typ == 'K' and move.color == 'magenta':
                if self.simulate(None, move.piece_0.color):
                    sh_del  = True
                move_ = 0
                if move.direc == 'E':
                    move_ = Move(move.piece_0, data_pieces[move.piece_0.row]['F'])
                elif move.direc == 'W':
                    move_ = Move(move.piece_0, data_pieces[move.piece_0.row]['D'])
                if self.simulate(move_, move.piece_0.color):
                    sh_del = True
            if sh_del:
                delete_set.append(move)
        for move in delete_set:
            temp_move_set.remove(move)

        for move in temp_move_set:
            self.move_set.append(move)

    def simulate(self, move, kingcolor):
        for row, row_lst in sim_data_pieces.items():
            for column, piece in row_lst.items():
                sim_data_pieces[row][column] = 0
        for row, row_lst in data_pieces.items():
            for column, piece in row_lst.items():
                piece_ = Piece()
                sim_data_pieces[row][column] = piece_
                piece_.color = piece.color
                piece_.typ = piece.typ
                piece_.row = piece.row
                piece_.column = piece.column
                piece_.has_moved = piece.has_moved
                piece_.en_passant = piece.en_passant

        if move:
            piece_a = Piece()
            piece_b = Piece()
            sim_data_pieces[move.piece_1.row][move.piece_1.column] = piece_b
            sim_data_pieces[move.piece_0.row][move.piece_0.column] = piece_a
            piece_a.color = 'yellow'
            piece_a.typ = ' '
            piece_a.has_moved = False
            piece_a.en_passant = False
            piece_b.color = move.piece_0.color
            piece_b.typ = move.piece_0.typ
            piece_b.has_moved = move.piece_0.has_moved
            piece_b.en_passant = move.piece_0.en_passant
            piece_a.sim_coor()
            piece_b.sim_coor()

        for row, row_lst in sim_data_pieces.items():
            for column, piece in row_lst.items():

                temp_move_set = []
                N = 0
                S = 0
                W = 0
                E = 0
                NW = 0
                NE = 0
                SW = 0
                SE = 0
                direc_router  = {
                    'N': N,
                    'S': S,
                    'W': W,
                    'E': E,
                    'NW': NW,
                    'NE': NE,
                    'SW': SW,
                    'SE': SE
                }

                if piece.typ == 'K':
                    for i in range(8):
                        for row, row_lst in sim_data_pieces.items():
                            if row_router[row] == row_router[piece.row] or row_router[row] == row_router[piece.row] + i or row_router[row] == row_router[piece.row] - i:
                                for column, piece_ in row_lst.items():
                                    if column_router[column] == column_router[piece.column] or column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                        if piece_ != piece:
                                            move = Move(piece, piece_)
                                            move.set_limit(move.set_direc(), i)
                                            if piece_.color != piece.color:
                                                if piece_.typ == ' ':
                                                    color = 'green'
                                                else:
                                                    color = 'red'
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 1
                                                move.set_color(color)
                                                temp_move_set.append(move)
                                            elif piece_.color == piece.color:
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 1

                if piece.typ == 'Q':
                    for i in range(8):
                        for row, row_lst in sim_data_pieces.items():
                            if row_router[row] == row_router[piece.row] or row_router[row] == row_router[piece.row] + i or row_router[row] == row_router[piece.row] - i:
                                for column, piece_ in row_lst.items():
                                    if column_router[column] == column_router[piece.column] or column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                        if piece_ != piece:
                                            move = Move(piece, piece_)
                                            move.set_limit(move.set_direc(), i)
                                            if piece_.color != piece.color:
                                                if piece_.typ == ' ':
                                                    color = 'green'
                                                else:
                                                    color = 'red'
                                                    if not direc_router[move.direc]:
                                                        direc_router[move.direc] = i
                                                move.set_color(color)
                                                temp_move_set.append(move)
                                            elif piece_.color == piece.color:
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = i

                if piece.typ == 'R':
                    for i in range(8):
                        for row, row_lst in sim_data_pieces.items():
                            if row_router[row] == row_router[piece.row] or row_router[row] == row_router[piece.row] + i or row_router[row] == row_router[piece.row] - i:
                                for column, piece_ in row_lst.items():
                                    if column_router[column] == column_router[piece.column] or column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                        if column == piece.column or row == piece.row:
                                            if piece_ != piece:
                                                move = Move(piece, piece_)
                                                move.set_limit(move.set_direc(), i)
                                                if piece_.color != piece.color:
                                                    if piece_.typ == ' ':
                                                        color = 'green'
                                                    else:
                                                        color = 'red'
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = i
                                                    move.set_color(color)
                                                    temp_move_set.append(move)
                                                elif piece_.color == piece.color:
                                                    if not direc_router[move.direc]:
                                                        direc_router[move.direc] = i

                if piece.typ == 'B':
                    for i in range(8):
                        for row, row_lst in sim_data_pieces.items():
                            if row_router[row] == row_router[piece.row] or row_router[row] == row_router[piece.row] + i or row_router[row] == row_router[piece.row] - i:
                                for column, piece_ in row_lst.items():
                                    if column_router[column] == column_router[piece.column] or column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                        if column != piece.column and row != piece.row:
                                            if piece_ != piece:
                                                move = Move(piece, piece_)
                                                move.set_limit(move.set_direc(), i)
                                                if piece_.color != piece.color:
                                                    if piece_.typ == ' ':
                                                        color = 'green'
                                                    else:
                                                        color = 'red'
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = i
                                                    move.set_color(color)
                                                    temp_move_set.append(move)
                                                elif piece_.color == piece.color:
                                                    if not direc_router[move.direc]:
                                                        direc_router[move.direc] = i

                if piece.typ == 'N':
                    knight_lst = [(2, 1), (1, 2)]
                    for a, b in knight_lst:
                        for row, row_lst in sim_data_pieces.items():
                            if row_router[row] == row_router[piece.row] + a or row_router[row] == row_router[piece.row] - a:
                                for column, piece_ in row_lst.items():
                                    if column_router[column] == column_router[piece.column] + b or column_router[column] == column_router[piece.column] - b:
                                        if piece_ != piece:
                                            move = Move(piece, piece_)
                                            move.set_limit(move.set_direc(), 2)
                                            if piece_.color != piece.color:
                                                if piece_.typ == ' ':
                                                    color = 'green'
                                                else:
                                                    color = 'red'
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 2
                                                move.set_color(color)
                                                temp_move_set.append(move)
                                            elif piece_.color == piece.color:
                                                if not direc_router[move.direc]:
                                                    direc_router[move.direc] = 2

                if piece.typ == 'P':
                    if piece.has_moved:
                        x=1
                    else:
                        x=2
                    if piece.color == 'white':
                        for i in range(8):
                            for row, row_lst in sim_data_pieces.items():
                                if row_router[row] == row_router[piece.row] - i:
                                    for column, piece_ in row_lst.items():
                                        if column_router[column] == column_router[piece.column]:
                                            if piece_ != piece:
                                                move = Move(piece, piece_)
                                                move.set_limit(move.set_direc(), i)
                                                if piece_.color != piece.color:
                                                    if piece_.typ == ' ':
                                                        color = 'green'
                                                        move.set_color(color)
                                                        if piece_.row == '8':
                                                            move.set_color('magenta')
                                                        temp_move_set.append(move)
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = x
                                                    else:
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = 1
                                                elif piece_.color == piece.color:
                                                    if not direc_router[move.direc]:
                                                        direc_router[move.direc] = x
                        for i in range(8):
                            for row, row_lst in sim_data_pieces.items():
                                if row_router[row] == row_router[piece.row] - i:
                                    for column, piece_ in row_lst.items():
                                        if column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                            if piece_ != piece:
                                                move = Move(piece, piece_)
                                                move.set_limit(move.set_direc(), i)
                                                if piece_.color != piece.color:
                                                    if piece_.typ != ' ':
                                                        color = 'red'
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = 1
                                                        move.set_color(color)
                                                        if piece_.row == '8':
                                                            move.set_color('magenta')
                                                        temp_move_set.append(move)
                                                    elif piece_.en_passant:
                                                        color = 'magenta'
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = 1
                                                        move.set_color(color)
                                                        temp_move_set.append(move)
                                                elif piece_.color == piece.color:
                                                    if not direc_router[move.direc]:
                                                        direc_router[move.direc] = 1
                        
                    elif piece.color == 'black':
                        for i in range(8):
                            for row, row_lst in sim_data_pieces.items():
                                if row_router[row] == row_router[piece.row] + i:
                                    for column, piece_ in row_lst.items():
                                        if column_router[column] == column_router[piece.column]:
                                            if piece_ != piece:
                                                move = Move(piece, piece_)
                                                move.set_limit(move.set_direc(), i)
                                                if piece_.color != piece.color:
                                                    if piece_.typ == ' ':
                                                        color = 'green'
                                                        move.set_color(color)
                                                        if piece_.row == '1':
                                                            move.set_color('magenta')
                                                        temp_move_set.append(move)
                                                        if not move.direc:
                                                            print(piece.row, piece.column, piece_.row, piece_.column)
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = x
                                                    else:
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = 1
                                                elif piece_.color == piece.color:
                                                    if not direc_router[move.direc]:
                                                        direc_router[move.direc] = x
                        for i in range(8):
                            for row, row_lst in sim_data_pieces.items():
                                if row_router[row] == row_router[piece.row] + i:
                                    for column, piece_ in row_lst.items():
                                        if column_router[column] == column_router[piece.column] + i or column_router[column] == column_router[piece.column] - i:
                                            if piece_ != piece:
                                                move = Move(piece, piece_)
                                                move.set_limit(move.set_direc(), i)
                                                if piece_.color != piece.color:
                                                    if piece_.typ != ' ':
                                                        color = 'red'
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = 1
                                                        move.set_color(color)
                                                        if piece_.row == '1':
                                                            move.set_color('magenta')
                                                        temp_move_set.append(move)
                                                    elif piece_.en_passant:
                                                        color = 'magenta'
                                                        if not direc_router[move.direc]:
                                                            direc_router[move.direc] = 1
                                                        move.set_color(color)
                                                        temp_move_set.append(move)
                                                elif piece_.color == piece.color:
                                                    if not direc_router[move.direc]:
                                                        direc_router[move.direc] = 1

                delete_set = []
                for move in temp_move_set:
                    limit = direc_router[move.direc]
                    if limit:
                        if move.dist > limit:
                            delete_set.append(move)

                for move in delete_set:
                    temp_move_set.remove(move)

                for move in temp_move_set:
                    if move.piece_1.color == kingcolor and move.piece_1.typ == 'K':
                        return True

moves = Move_set()

data_squares = {
    '8': {'A': Square(), 'B': Square(), 'C': Square(), 'D': Square(), 'E': Square(), 'F': Square(), 'G': Square(), 'H': Square()},
    '7': {'A': Square(), 'B': Square(), 'C': Square(), 'D': Square(), 'E': Square(), 'F': Square(), 'G': Square(), 'H': Square()},
    '6': {'A': Square(), 'B': Square(), 'C': Square(), 'D': Square(), 'E': Square(), 'F': Square(), 'G': Square(), 'H': Square()},
    '5': {'A': Square(), 'B': Square(), 'C': Square(), 'D': Square(), 'E': Square(), 'F': Square(), 'G': Square(), 'H': Square()},
    '4': {'A': Square(), 'B': Square(), 'C': Square(), 'D': Square(), 'E': Square(), 'F': Square(), 'G': Square(), 'H': Square()},
    '3': {'A': Square(), 'B': Square(), 'C': Square(), 'D': Square(), 'E': Square(), 'F': Square(), 'G': Square(), 'H': Square()},
    '2': {'A': Square(), 'B': Square(), 'C': Square(), 'D': Square(), 'E': Square(), 'F': Square(), 'G': Square(), 'H': Square()},
    '1': {'A': Square(), 'B': Square(), 'C': Square(), 'D': Square(), 'E': Square(), 'F': Square(), 'G': Square(), 'H': Square()}
}

data_pieces = {
    '8': {'A': Piece(), 'B': Piece(), 'C': Piece(), 'D': Piece(), 'E': Piece(), 'F': Piece(), 'G': Piece(), 'H': Piece()},
    '7': {'A': Piece(), 'B': Piece(), 'C': Piece(), 'D': Piece(), 'E': Piece(), 'F': Piece(), 'G': Piece(), 'H': Piece()},
    '6': {'A': Piece(), 'B': Piece(), 'C': Piece(), 'D': Piece(), 'E': Piece(), 'F': Piece(), 'G': Piece(), 'H': Piece()},
    '5': {'A': Piece(), 'B': Piece(), 'C': Piece(), 'D': Piece(), 'E': Piece(), 'F': Piece(), 'G': Piece(), 'H': Piece()},
    '4': {'A': Piece(), 'B': Piece(), 'C': Piece(), 'D': Piece(), 'E': Piece(), 'F': Piece(), 'G': Piece(), 'H': Piece()},
    '3': {'A': Piece(), 'B': Piece(), 'C': Piece(), 'D': Piece(), 'E': Piece(), 'F': Piece(), 'G': Piece(), 'H': Piece()},
    '2': {'A': Piece(), 'B': Piece(), 'C': Piece(), 'D': Piece(), 'E': Piece(), 'F': Piece(), 'G': Piece(), 'H': Piece()},
    '1': {'A': Piece(), 'B': Piece(), 'C': Piece(), 'D': Piece(), 'E': Piece(), 'F': Piece(), 'G': Piece(), 'H': Piece()}
}

sim_data_pieces = {
    '8': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '7': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '6': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '5': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '4': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '3': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '2': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '1': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
}

widget_squares = {
    '8': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '7': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '6': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '5': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '4': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '3': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '2': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '1': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
}

widget_pieces = {
    '8': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '7': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '6': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '5': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '4': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '3': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '2': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0},
    '1': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0}
}

row_router = {
    '8': 0,
    '7': 1,
    '6': 2,
    '5': 3,
    '4': 4,
    '3': 5,
    '2': 6,
    '1': 7,
}

column_router = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 7,
}

clrs = ['green', 'red', 'magenta']

def set_atts():
    global c
    clr = 'yellow'
    c = 0
    for row, row_lst in data_squares.items():
        for column, square in row_lst.items():
            square.set_id(c)
            square.set_color(clr)
            square.coor()
            data_pieces[row][column].set_square(square)
            c+=1
            clr = 'blue' if clr == 'yellow' else 'yellow'
        clr = 'blue' if clr == 'yellow' else 'yellow'
    c = 0
    for row, row_lst in data_pieces.items():
        for column, piece in row_lst.items():
            data_squares[row][column].set_piece(piece)
            piece.set_id(c)
            piece.coor()
            c+=1
    royal = 'RNBQKBNR'
    for num, piece in enumerate(data_pieces['8'].values()):
        piece.set_color_typ('black', royal[num])
    for num, piece in enumerate(data_pieces['1'].values()):
        piece.set_color_typ('white', royal[num])
    for num, piece in enumerate(data_pieces['7'].values()):
        piece.set_color_typ('black', 'P')
    for num, piece in enumerate(data_pieces['2'].values()):
        piece.set_color_typ('white', 'P')
    for row, row_lst in data_pieces.items():
        if row in '3456':
            for column, piece in row_lst.items():
                piece.set_color_typ(piece.square.color, ' ')

def start():
    set_atts()
    board.draw_squares()
    board.draw_pieces()

start()

win.mainloop()


