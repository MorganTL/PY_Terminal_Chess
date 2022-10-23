import chess, click, time

def Title_screen(option = None):

    click.secho(r"""  .oooooo.   oooo                                    
 d8P'  `Y8b  `888
888           888 .oo.    .ooooo.   .oooo.o  .oooo.o 
888           888P"Y88b  d88' `88b d88(  "8 d88(  "8 
888           888   888  888ooo888 `"Y88b.  `"Y88b.  
`88b    ooo   888   888  888    .o o.  )88b o.  )88b 
 `Y8bood8P'  o888o o888o `Y8bod8P' 8""888P' 8""888P'""", fg="bright_blue")

    color = ["bright_white","bright_white", "bright_white", "bright_white"]
    if option == None or not option.isnumeric() or int(option) > 4:
        click.secho("1: Local Multiplayer", fg=f"{color[0]}")
        click.secho("2: Play with AI", fg=f"{color[1]}")
        click.secho("3: Queens game", fg=f"{color[2]}")
        click.secho("4: Exit", fg=f"{color[3]}")
        return False
    else:
        color[int(option)-1] = "bright_green"
        click.secho("1: Local Multiplayer", fg=f"{color[0]}")
        click.secho("2: Play with AI", fg=f"{color[1]}")
        click.secho("3: Queens game", fg=f"{color[2]}")
        click.secho("4: Exit", fg=f"{color[3]}")
        return True

def main():
    click.clear()
    Title_screen()
    click.secho("Which mode you want to play(1-4): ", fg="bright_white", nl=False)
    s = input()
    while True:
        click.clear()
        if Title_screen(s):
            break
        click.secho("Invalid Input, Enter again (1-4): ", fg="bright_red",nl=False)
        s = input()
    time.sleep(0.5)
    if s == "1":
        chess.main()
    elif s == "2":
        pass
    elif s == "3":
        pass
    elif s == "4":
        pass

    # chess.main()
if __name__ == "__main__":
    main()
    click.pause()



    