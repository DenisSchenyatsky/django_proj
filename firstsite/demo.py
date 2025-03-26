def fact(n):
    if n < 3:
        return n
    return n * fact(n-1)

def main():
    print(fact(5))
    print(fact(10))
    
if __name__=="__main__":
    main()