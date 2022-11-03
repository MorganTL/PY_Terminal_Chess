import src
import click, time, json


def draw_title_screen(options_dict:dict):
    """
    Draw titel screen with options list

    options_dict: {1:["Name for option 1", "foreground_color"], 2:["Name for option 2", "foreground_color"] etc...}
    """

    click.secho(r"""  .oooooo.   oooo                                    
 d8P'  `Y8b  `888
888           888 .oo.    .ooooo.   .oooo.o  .oooo.o 
888           888P"Y88b  d88' `88b d88(  "8 d88(  "8 
888           888   888  888ooo888 `"Y88b.  `"Y88b.  
`88b    ooo   888   888  888    .o o.  )88b o.  )88b 
 `Y8bood8P'  o888o o888o `Y8bod8P' 8""888P' 8""888P'""", fg="bright_blue")
    
    click.secho()

    options_len = len(options_dict)

    for k in range(1,options_len+1):
        click.secho(f"{k}: {options_dict[k][0]}", fg = options_dict[k][1])
    

def locate_gamesave(filepath:str):
    """
    return True when json save is not empty
    """
    try:
        data = json.load(open(filepath))
        return any(data)
    except FileNotFoundError:
        return False

def sub_menu_loop(user_input:str):
    """
    Sub menu has 3 option to choose from
    1) Continue last game
    2) New Game
    3) Go back to main menu

    user_input: 1 = "Local multiplayer", 2 =  "Play with AI", 3 = "N Queens Puzzle"
    """
    # sub_menu start here
    sub_menu_options = {
        1: ["Continue last game", "reset"],
        2: ["New Game", "reset"],
        3: ["Back ↩", "reset"],
    }

    if user_input == "1": # lcoal play
        game_message = "Local multiplayer"
    elif user_input == "2": # play with ai
        game_message = "Play with AI"
    elif user_input == "3": # play with ai
        game_message = "N Queens Puzzle"


    click.clear()
    draw_title_screen(sub_menu_options)
    

    warning_message = click.style("\n")
    menu_message =  click.style(f" - Which mode you want to play(1-{len(sub_menu_options)}): ")
    message = warning_message + game_message + menu_message

    click.secho(message, nl=False)
    user_input = input()
    
    while True:
        if user_input in map(str, range(1, len(sub_menu_options)+1)):
            sub_menu_options[int(user_input)][1] = "green"
            click.clear()
            draw_title_screen(sub_menu_options)
            time.sleep(0.5)
            break
        warning_message = click.style("\nInvalid input! ", fg = "bright_red")
        message = warning_message + game_message + menu_message
        click.secho(message, nl=False)
        user_input = input()
    
    # !!Important!! Enter game with submenu here
    if game_message == "Local multiplayer":
        if user_input == "1":
            src.play_locally(True)
        elif user_input == "2":
            src.play_locally()
    elif game_message == "Play with AI":
        if user_input == "1": # continue from old save file
            src.play_with_AI(True)
        elif user_input == "2":
            src.play_with_AI()
    elif game_message == "N Queens Puzzle":
        if user_input == "1": # continue from old save file
            src.play_n_queen(8, True)
        elif user_input == "2":
            src.play_n_queen()


def main():
    # Main menu loop
    while True:
        
        local_play_savefile = locate_gamesave("./src/save_file/local_play.json")
        ai_play_savefile = locate_gamesave("./src/save_file/ai_play.json")
        n_queen_savefile = locate_gamesave("./src/save_file/n_queen.json")

        main_menu_options = {
            1: ["Local multiplayer", "reset"],
            2: ["Play with AI", "reset"],
            3: ["N Queens Puzzle", "reset"],
            4: ["AI vs AI", "reset"],
            5: ["Exit", "reset"],
        }

        click.clear()
        draw_title_screen(main_menu_options)
        
        warning_message = click.style("\n")
        menu_message =  click.style(f"Which mode you want to play(1-{len(main_menu_options)}): ")
        message = warning_message + menu_message

        click.secho(message, nl=False)
        user_input = input()
        
        while True:
            if user_input in map(str, range(1, len(main_menu_options)+1)):
                main_menu_options[int(user_input)][1] = "green"
                click.clear()
                draw_title_screen(main_menu_options)
                time.sleep(0.5)
                break
            warning_message = click.style("\nInvalid input! ", fg = "bright_red")
            message = warning_message + menu_message
            click.secho(message, nl=False)
            user_input = input()
            

        # !!Important!! Enter game with No sub menu HERE
        if user_input == str(len(main_menu_options)): # exit
            click.pause("Press any key to exit...")
            break
        elif user_input == "1" and not local_play_savefile: # local play
            src.play_locally()
            continue
        elif user_input == "2" and not ai_play_savefile: # play with ai
            src.play_with_AI()
            continue
        elif user_input == "3" and not n_queen_savefile: # N Queens Puzzlee
            src.play_n_queen()
            continue
        elif user_input == "4": # ai vs ai mode
            src.AI_vs_AI()
            continue
        
        sub_menu_loop(user_input)

if __name__ == "__main__":
    main()
    



    