import os
import time

from strategy import Strategy


def main():
    print("Enter the name of the equity:")
    script = input().strip()
    print(f"Getting data for the following equity: {script}")
    strategy = Strategy(script)
    data1 = strategy.get_signals()
    print(data1.head(50))
    
if __name__ == "__main__":
    main()