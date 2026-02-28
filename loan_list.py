# This class represents the users loans
from database import db
from loan import Loan


class LoanList():

    def __init__(self, user_id):

        self.loans = []

        loans_db = db.get_loans(user_id)

        for loan in loans_db:

            loan_id = loan[0]
            loan_name = loan[2]
            min_payment = loan[3]
            type = loan[4]
            late_fee = loan[5]
            p_amount = loan[6]
            ir = loan[7]
            it = loan[8]
            term_length = loan[9]
            amount_payed = loan[10]

            self.loans.append(Loan(loan_id, loan_name, min_payment, type, late_fee, p_amount, ir, it, term_length, amount_payed))

        self.loan_total = self.Calculate_Loan_Total()

        self.num_loans = len(self.loans)


    def Calculate_Loan_Total(self):

        total_amount = 0

        for loan in self.loans:

            total_amount = total_amount + loan.p_amount

        return total_amount

    def Calculate_Average_Loan_Size(self):

        total_amount = self.Calculate_Loan_Total()

        if self.num_loans == 0:

            return 0

        return total_amount / self.num_loans


    def Create_Post(self):

        loan_total = self.Calculate_Loan_Total()
        avg_loan = self.Calculate_Average_Loan_Size()

        post = {'total_amount':loan_total, 'avg_loan':avg_loan}

        return post
