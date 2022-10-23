
import time, click

def main():

    s = 0
    y = "B"
    while True:
        if s%2 == 0: click.secho(f"\r S is {s}\r", nl=False )
        else: click.secho(f"\r y is {y}\r", nl=False, bg = "bright_green" )
        s+= 1
        
        time.sleep(0.1)

if __name__ == "__main__":
    main()