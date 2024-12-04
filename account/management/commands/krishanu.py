from django.core.management.base import BaseCommand

class Command(BaseCommand):
    # help="Prints,Hello world!"
    help ="Add,two numbers"
    
    def add_arguments(self,parser):
        # parser.add_argument('name',type=str, help='Input name to be printed')
        # parser.add_argument('-a','--add',nargs=2,type=int,help="Two numbers added")
        parser.add_argument('-o',type=str,choices=['add','multiply'], help='Operation to perform')
        parser.add_argument('numbers',nargs=2,type=int,help="Two numbers for operations")
        
        
    def handle(self, *args, **kwargs):
        # name=kwargs['name']
        # print(f"Hello, World {name}")
        # numbers=kwargs['add']
        # if numbers:
        #     num1,num2=numbers
        #     result=num1 +num2
        #     print(f"The sum of {num1} and {num2} is {result}")
        # else:
        #     print("Please provide the numbers")    
        operations=kwargs['o']
        numbers=kwargs['numbers']
       
        num1,num2=numbers
        
        if operations == 'add':
            result = num1 + num2
            print(f'The sum of {num1} and {num2} is {result}')
        elif operations=="multiply":
            result = num1 * num2
            print(f'The multiply of {num1} and {num2} is {result}')
        else:
            print('Invalid operation. Use add, multiply' )    
            
            