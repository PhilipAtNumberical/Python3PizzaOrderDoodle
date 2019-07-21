import re
import sys
from time import sleep
import subprocess
import platform

#Variables
MaximumNumberCanOrder = 6
DeliverySurcharge = 15
ReturingPickupCustomerDiscount = 0.9
FirstThreeItemPrice = 5
RemainingItemPrice = 8


#Pizza Menu As a Dictionary
PizzaAvaliable = (
    {"name":"Margherita"},
    {"name":"Marinara"},
    {"name":"Quattro Stagioni"},
    {"name":"Carbonara"},
    {"name":"Frutti di Mare"},
    {"name":"Quattro Formaggi"},
    {"name":"Crudo"},
    {"name":"Napoli"},
    {"name":"Pugliese"},
    {"name":"Montanara"},
    )

# special exception, only to be use when order is cancel.  meant to be empty
# needed to complete the try-catch function, when this is raised, do nothing, just let it passed
class CancelOrder(Exception):
    pass


# class with default order details
class Order():
    def __init__(self):
        self.pickup = True
        self.returningcustomer = False

        self.name = ""
        self.address = None
        self.phone = None

        self.number_pizzas = 0
        self.pizzas = []

        self.total_cost = 0

def get_input(regex, input_message=None, error_message=None, ignore_case=True):
    # loop forever until termination creteria met.
    while True:
        # input to validate, input prompt is as specified
        u_input = input(str(input_message))

        # check if the user wants to quit or cancel the order
        if u_input.lower() == "t" or u_input.lower() == "exit":
            print("Closing Program")
            sleep(2)
            sys.exit()
        elif u_input.lower() == "x" or u_input.lower() == "cancel":
            raise CancelOrder()

        # check if the input matches the regex provided
        # if input matches regex and/or part of the ignore case, break out from this function
        # and don't throw error
        if ignore_case:
            if re.match(regex, u_input, re.IGNORECASE):
                break
        else:
            if re.match(regex, u_input):
                break

        # otherwise if input doesn't match regex, display the error message has been specified
        if error_message:
            print(str(error_message))

    return u_input


def print_order(order):
    print("| Name: {}".format(order.name))
    print("| Order type: {}".format("Pickup" if order.pickup else "Delivery"))
    if not order.pickup:
        print("| Delivery address: {}".format(order.address))
        print("| Customer phone number: {}".format(order.phone))
    print("|\n| Order summary:\t\t\t\tPrice each:\tSubtotal:")
    for pizza in order.pizzas:
        print("| \t{}x {:<22}".format(
            pizza['amount'], pizza['name']))

    if not order.pickup:
            print("| \tDelivery charge\t\t\t\t\t$ {:>5.2f}".format(
                DeliverySurcharge))
    print("| {:61}--------".format(""))
    print("| {:54} Total: ${:.2f}".format("", order.total_cost))


# this function is used for padding the input string
# take the input string and break each word is a line itself, with width as length, padded with = and captalised 1st letter

def WelcomeMessage(text, *, width=65, padding='='):

    return '\n'.join([f'{word.capitalize():{padding}^{width}}' for word in text.split()])


# this function has the same functionality as the WelcomeMessage function, but with different length size
def MainHeading(text, *, width=11, padding='='):
    return ''.join([f'{word.capitalize():{padding}^{width}}' for word in text.split()])

# this function has the same functionality as the WelcomeMessage function, but with different length size
# and uses ' ' instead of '=' as padding
def SubHeading(text, *, width=1, padding=' '):
    return ' '.join([f'{word.capitalize():{padding}^{width}}' for word in text.split()])    

# this function is used to display some useful information, only inteded to be used the the program is 1st run
# statements is like a array of strings, that can be joined together using the .join function
def UsefulInformation(): 
    statements = [
                  '\nFirst Three (3) Pizza ${} each, All Other Pizza ${} each.'.format(FirstThreeItemPrice, RemainingItemPrice),
                  'Maximum {} Pizza Per Order'.format(MaximumNumberCanOrder),
                  'Extra ${} Surcharge For Delivery'.format(DeliverySurcharge),
                  '\nAt Anytime When Ordering: ',
                  '\nType "X" or "Cancel" (Without Quotes) To Cancel Your Order.',
                  '\nType "T" or "Exit" (Without Quotes) To Exit.'
                  ]
                
     
    return '\n'.join(statements)

def PrintMenu():
    #sort pizzas alphabetically
    pizzalist = sorted(PizzaAvaliable, key=lambda k: (k["name"]))
    print(MainHeading("Pizza Avaliable"))

    keys = []
    vals = []

    for pizzas in pizzalist:
        val = []
        for k,v in pizzas.items():
            keys.append(k)
            val.append(v)
        vals.append(val)

    #Print Avaliable Pizzas Stored In List
    print(list(pizzas.fromkeys(keys)))
    for v in vals:
        print(v)
    

def main(): 
    print(WelcomeMessage("Welcome To Dream Pizzas"))
    print(UsefulInformation())
    PrintMenu()


    # list to hold all completed orders
    orders = []

    # sorts pizza list =alphabetically
    pizzas_available = sorted(
        PizzaAvaliable,
        key=lambda k: (k["name"]))

    # keep getting orders, only exits through sys.exit()
    while True:
        # try ... except to catch CancelOrder exception
        try:
            print("\nNew Order")
            order = Order()

            while True:

                # get delivery/pickup type
                user_input = get_input(
                    r"[A-Z]+$",
                    "Pickup or Delivery? \n(For Pickup Enter p or pickup, For Delivery Enter d or delivery): ",
                    "Invalid Input! For Pickup Enter: p or pickup, For Delivery Enter: d or delivery")
                if user_input.lower()=="d" or user_input.lower()=="delivery":
                    user_input2 = get_input(
                        r"[A-Z]+$",
                        "For Delivery ${} Surcharge Will Be Added, Do You Want To Proceed? \n(Enter y Or yes To Proceed With Delivery, Enter n or no To Change To Pickup): ".format(DeliverySurcharge),
                        "Invalid Input! For Proceed With Pickup Enter: y or yes, To Change To Pickup Enter: n or no"
                        )
                    if user_input2.lower()=="y" or user_input2.lower()=="yes":
                        order.pickup = False
                        break
                    else:
                        order.pickup = True
                        break
                elif user_input.lower()=="p" or user_input.lower()=="pickup":
                    order.pickup = True
                    break
                else:
                    print("Invalid Input! For Pickup Enter: p Or pickup, For Delivery Enter: d or delivery")

            # get name of the customer
            order.name = get_input(
                r"[A-Z]+$",
                "Enter customer name: ",
                "Name must only contain letters")

            if order.pickup:
                user_input = get_input(
                    r"[A-Z]+$",
                    "{}, Are You An Returning Customer?  \n(Enter y Or yes For Returning Customer, Enter n Or no For New Customer): ".format(order.name),
                    "Invalid Input! Enter y Or yes For Returning Customer, Enter n Or no For New Customer"
                    )
                if user_input.lower()=="y" or user_input.lower()=="yes":
                    discount = (1-ReturingPickupCustomerDiscount)*100
                    print("Returning Cusomter Recieves {:.2f}% discounts".format(discount))
                    order.returningcustomer = True
                else:
                    order.returningcustomer = False

            # get address, phone number info (if the customer wants delivery)
            if not order.pickup:
                order.address = get_input(
                    r"[ -/\w]+$",
                    "Delivery address: ",
                    "Address must only contain alphanumeric characters")
                order.phone = get_input(
                    r"\d+$",
                    "Phone number: ",
                    "Phone number must only contain numbers")

            # get number of pizzas to order,
            # make sure it is more than 0,less than max_pizzas
            while True:
                user_input = get_input(
                    r"\d$",
                    "Number of pizzas to order: ",
                    "Must be a digit, {} or less".format(MaximumNumberCanOrder))
                user_input = int(user_input)
                if 0 < user_input <= MaximumNumberCanOrder:
                    order.number_pizzas = user_input
                    break
                else:
                    print("Must be a digit, {} or less (but more than 0)".format(MaximumNumberCanOrder))

            # print menu (each pizza is assigned a number)
            print("\nWhat pizzas would you like to order?")
            for i, pizza in enumerate(pizzas_available):
                # each pizza's number is its index (i) + 1,
                # so the first pizza is 1
                print("{}: {}".format(str(i+1).zfill(2), pizza['name']))

            print("\nEnter your selection number for each pizza you want to buy")
            for i in range(order.number_pizzas):
                while True:
                    string = "Pizza #{} of {}:".format(i+1, order.number_pizzas)
                    user_input = get_input(
                        r"\d\d?$",
                        string,
                        "Pizza selection number must"
                        "correspond to those listed above")
                    user_input = int(user_input)
                    try:
                        if user_input == 0:
                            raise IndexError
                        # selects the pizza based on user_input
                        to_add = pizzas_available[user_input-1]

                        # if the pizza has already been ordered,
                        # increment the amount ordered
                        for ordered in order.pizzas:
                            if to_add["name"] == ordered["name"]:
                                ordered["amount"] += 1
                                break
                        # else add the pizza to the order list
                        else:
                            order.pizzas.append(to_add)
                            order.pizzas[-1]["amount"] = 1

                        # if there has been no error,
                        # input is valid, break from the while loop
                        break

                    except IndexError:
                        print("Pizza selection number must"
                            "correspond to those listed above")

            if order.number_pizzas <= 3:
                order.total_cost = order.number_pizzas * FirstThreeItemPrice
            else:
                order.total_cost = (3*FirstThreeItemPrice) + ((order.number_pizzas - 3) * RemainingItemPrice)
                
            if not order.pickup:
                    order.total_cost += DeliverySurcharge
            if order.pickup:
                if order.returningcustomer:
                    order.total_cost = order.total_cost * ReturingPickupCustomerDiscount

            # add order to list of orders
            #orders.append(order)
            #print("\nOrder saved. Order was:")
            #print_order(order)

            print("Your Order: ")
            print_order(order)
            
            # r"$|(?:Y|N).*" is the regex, i.e. if user input anything other then Y/ yes or N/No it will trigger the error message
            user_input = get_input(
                r"$|(?:Y|N).*",
                "Would You Like To Repeat This Order? (Enter y or yes For Repeating This Other, Enter n or no For One Time Purchase): ",
                "Only yes/or responses allowed"
                )

            # r"[+]?\d*\.\d+|\d+" is the regex, this regex only accepts \d (number) input, otherwise will throw error message
            if user_input.lower()=="y" or user_input.lower()=="yes":
              user_input2 = float(get_input(
                  r"[+]?\d*\.\d+|\d+",
                  "How Many Day(s) Would You Like To Repeat This Order? ",
                  "Invalid Input! Please Enter A Positive Digit Larger Than 0"
                  ))
              order.total_cost = order.total_cost*user_input2
              orders.append(order)
              print("\nOrder updated and saved. Your New Order Receipt:")
              print_order(order)
            else:
              orders.append(order)
              print("\nOrder saved. Order was:")
              print_order(order)
              
            # r"$|(?:Y|N|O).*" is the regex, i.e. if user input anything other then Y/ yes, N/No or orders it will trigger the error message
            user_input = get_input(
                r"$|(?:Y|N|O).*",
                "Would you like to enter another order or view all"
                    "previous orders? (Please Enter Either: Y/N/Orders): ",
                "Only yes/no or \"orders\" responses allowed")
            if user_input.lower()=="orders" or user_input.lower()=="o":
                for i, order in enumerate(orders):
                    print("-" * 73)
                    print_order(order)
                    if i == len(orders) + 1:
                        print("-" * 73)
            elif user_input.lower().startswith("n"):
                print("Exiting Program")
                sleep(2)
                sys.exit()

        except CancelOrder:
            try:
                # r"$|(?:Y|N).*" is the regex, i.e. if user input anything other then Y/ yes or N/No it will trigger the error message
                print("\nOrder cancelled")
                user_input = get_input(
                    r"$|(?:Y|N).*",
                    "Would you like to enter another order? y/n: ",
                    "Only yes or no responses allowed")
                if user_input.lower()=="no" or user_input.lower()=="n":
                    print("Exiting Program")
                    sleep(2)                    
                    sys.exit()

            except CancelOrder:
                print("Type 'T' or 'exit' to exit the program")

main()
