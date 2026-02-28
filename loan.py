# this class represents a single loan

class Loan:

    def __init__(self, id, name, min_payment, type, late_fee, p_amount, ir, it, term_length):

        self.id = id
        self.name = name
        self.min_payment = min_payment
        self.type = type
        self.late_fee = late_fee
        self.p_amount = p_amount
        self.ir = ir
        self.it = it
        self.term_length = term_length
