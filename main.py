import random
import mysql.connector
import sql_details

username = sql_details.username
password = sql_details.password

mydb = mysql.connector.connect(
    host="localhost",
    user=username,
    password=password,
    database="bank_management")

naira = u'\u20a6'


def open_account():
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    user_name = input("Username Name: ")
    acc_no = random.randint(2111111111, 2999999999)
    print(f'Welcome {first_name}, your new account number is {acc_no}')
    dob = input("Enter Date of Birth e.g: 1999-12-30: ")
    mobile_number = int(input("Enter Mobile Number: "))
    address = input("Enter Your Address: ")
    opening_balance = float(input("Enter Opening Balance: "))
    user_data1 = (first_name, last_name, user_name, acc_no, dob, mobile_number, address, opening_balance)
    user_data2 = (first_name, last_name, acc_no, opening_balance)
    sql1 = '''INSERT INTO ACCOUNT (first_name, last_name, user_name, acc_no, dob, mobile_number, address, 
    opening_balance) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
    sql2 = 'INSERT INTO BALANCE (First_name, Last_name, Acc_no, Balance) VALUES (%s,%s,%s,%s)'
    database = mydb.cursor()
    database.execute(sql1, user_data1)
    database.execute(sql2, user_data2)
    mydb.commit()
    print("Account Successfully Created.")
    main()


def make_deposit():
    acc_no = int(input("Enter Your Account Number: "))
    amount = float(input("Enter Deposit Amount: "))
    a = "select balance from Balance where Acc_No=%s"
    data = (acc_no,)
    database = mydb.cursor()
    database.execute(a, data)
    result = database.fetchone()
    t = result[0] + amount
    sql = "UPDATE balance SET Balance=%s WHERE Acc_No=%s"
    d = (t, acc_no)
    database.execute(sql, d)
    mydb.commit()
    print(f"{naira}{amount} was successfully Deposited into {acc_no}")
    main()


def withdrawal():
    acc_no = int(input("Enter Your Account Number: "))
    amount = float(input("Enter Deposit Amount: "))
    a = "select balance from balance where Acc_No=%s"
    data = (acc_no,)
    database = mydb.cursor()
    database.execute(a, data)
    result = database.fetchone()
    t = result[0] - amount
    sql = 'UPDATE balance SET balance=%s WHERE Acc_No=%s'
    d = (t, acc_no)
    database.execute(sql, d)
    mydb.commit()
    print(f"{naira}{amount} was successfully withdrawn from {acc_no}")
    charges(acc_no)

    main()


def transfer():
    acc_no = int(input("Enter Your Account Number: "))
    amount = float(input("Enter Transfer Amount: "))
    a = "select balance from balance where Acc_No=%s"
    data = (acc_no,)
    database = mydb.cursor()
    database.execute(a, data)
    result = database.fetchone()
    t = result[0] - amount
    sql = 'UPDATE balance SET balance=%s WHERE Acc_No=%s'
    d = (t, acc_no)
    database.execute(sql, d)

    # Receiver Info and Process
    rev_acc_no = int(input("Enter Receiver's AccNo.: "))
    b = "select balance from balance where Acc_No=%s"
    data2 = (rev_acc_no,)
    database = mydb.cursor()
    database.execute(b, data2)
    result = database.fetchone()
    m = result[0] + amount
    sql2 = 'UPDATE balance SET balance=%s WHERE Acc_No=%s'
    r = (m, rev_acc_no)
    database.execute(sql2, r)
    confirm(acc_no, rev_acc_no, amount)
    mydb.commit()

    print(f"You transferred {naira}{amount} from your account {acc_no} to {rev_acc_no}")
    charges(acc_no)
    main()


def confirm(acc_no, rev_acc_no, amount):
    a = "SELECT * from balance WHERE Acc_No=%s"
    data = (acc_no,)
    database = mydb.cursor()
    database.execute(a, data)
    result = database.fetchall()
    for name in result:
        first_name = name[0]
        last_name = name[1]

    a = "SELECT * from balance WHERE Acc_No=%s"
    data = (rev_acc_no,)
    database = mydb.cursor()
    database.execute(a, data)
    result = database.fetchall()
    for name in result:
        f_name = name[0]
        l_name = name[1]
    print(f"Are you sure you want transfer {amount} from {last_name} {first_name} to {l_name} {f_name}?")
    user_input = input("Enter 'Y' for YES & 'N' for NO:  ")

    if user_input == "y" or "Y":
        pass
    else:
        print("Transfer Cancelled!")
        main()


def charges(acc_no):
    amount = 10.0
    a = "select balance from balance where Acc_No=%s"
    data = (acc_no,)
    database = mydb.cursor()
    database.execute(a, data)
    result = database.fetchone()
    t = result[0] - amount
    sql = 'UPDATE balance SET balance=%s WHERE Acc_No=%s'
    d = (t, acc_no)
    database.execute(sql, d)
    mydb.commit()

    # Receiver Info and Process
    rev_acc_no = 2664999078
    b = "select balance from balance where Acc_No=%s"
    data2 = (rev_acc_no,)
    database = mydb.cursor()
    database.execute(b, data2)
    result = database.fetchone()
    m = result[0] + amount
    sql2 = 'UPDATE balance SET balance=%s WHERE Acc_No=%s'
    r = (m, rev_acc_no)
    database.execute(sql2, r)
    mydb.commit()

    print(f"Service Changed of {naira}{amount} was debited")
    main()


def balance_inqiry():
    acc_no = int(input("Enter Your Account Number: "))
    a = 'SELECT * FROM balance WHERE Acc_No=%s'
    data = (acc_no,)
    database = mydb.cursor()
    database.execute(a, data)
    result = database.fetchall()
    for row in result:
        first_name = row[0]
        last_name = row[1]
        acc = row[2]
        balance = row[3]
        print('*' * 50 + '\n')
        print('Account Balance')
        print('*' * 50)
        print(f'Full Name: {last_name} {first_name}\n')
        print(f'Account Number: {acc}\n')
        print(f'Current Balance: {naira}{balance}')
        print('*' * 50 + '\n')
    main()


def customer_details():
    acc_no = int(input("Enter Your Account Number: "))
    a = 'SELECT * FROM account WHERE Acc_No = %s'
    data = (acc_no,)
    database = mydb.cursor()
    database.execute(a, data)
    result = database.fetchall()

    for row in result:
        first_name = row[0]
        last_name = row[1]
        user_name = row[2]
        acc_no = row[3]
        date_of_birth = row[4]
        mobile_number = row[5]
        address = row[6]
        open_bal = row[7]
        print('*' * 50)
        print('Account Info')
        print('*' * 50)

        print(f'\nFirst Name: {first_name} \n')
        print(f'Last Name: {last_name}\n')
        print(f'Username: {user_name}\n')
        print(f'Account Number: {acc_no}\n')
        print(f'Date of Birth: {date_of_birth}\n')
        print(f'Mobile Number: {mobile_number}\n')
        print(f'Address: {address}\n')
        print(f'Opening Balance: {naira}{open_bal}\n')

    b = 'SELECT * FROM balance WHERE Acc_No=%s'
    database2 = mydb.cursor()
    database2.execute(b, data)
    result2 = database2.fetchall()
    for row in result2:
        balance = row[3]
        print(f'Current Balance: {naira}{balance}')
        print('*' * 50 + '\n')
    main()


def all_accounts():
    counters = 0
    a = 'SELECT * FROM balance'
    database = mydb.cursor()
    database.execute(a)
    result = database.fetchall()
    for row in result:
        counters += 1
        first_name = row[0]
        last_name = row[1]
        acc = row[2]
        balance = row[3]
        print('*' * 50 + '\n')
        print('Account Balance')
        print('*' * 50)
        print(f'Full Name: {last_name} {first_name}\n')
        print(f'Account Number: {acc}\n')
        print(f'Current Balance: {naira}{balance}')
        print('*' * 50 + '\n')
    print(f'There are {counters} Customers in Database')
    main()


def close_account():
    acc_no = int(input("Enter Your Account Number: "))
    sql1 = 'delete from account where Acc_No=%s'
    sql2 = 'delete from balance where Acc_No=%s'
    print(f'are you sure you want to DELETE  the account {acc_no}? Y/N')
    userinput = input("Enter Y for yes or N for no: ")
    if userinput == "y":
        data = (acc_no,)
        database = mydb.cursor()
        database.execute(sql1, data)
        database.execute(sql2, data)
        mydb.commit()
        print('Account DELETED Successfully')
    else:
        print("Account DELETING Failure")

    main()


def main():
    print(
        '''
        WELCOME TO WeGo Bank
        ********************
        CHOOSE AN OPTION:
        1. OPEN NEW ACCOUNT
        2. MAKE DEPOSIT
        3. MAKE TRANSFER
        4. MAKE A WITHDRAWAL
        5. CHECK BALANCE
        6. CUSTOMER DETAILS
        7. CLOSE ACCOUNT
        
        ''')

    choice = input("Enter 1-6 to start a transaction.: ")

    if choice == '1':
        open_account()
    elif choice == '2':
        make_deposit()
    elif choice == '3':
        transfer()
    elif choice == '4':
        withdrawal()
    elif choice == '5':
        balance_inqiry()
    elif choice == '6':
        customer_details()
    elif choice == '7':
        close_account()
    elif choice == '8':
        all_accounts()
    else:
        print("you have entered an invalid choice. Please Enter 1-6 to make a transaction.")


main()
