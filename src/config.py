import json
import logging

"""
____Note____
create a config.json file using the
config.example.json provided &
fill in the values.
"""
with open("config.json", "r") as file:
    config = json.load(file)


log_level_info = {
    "logging.DEBUG": logging.DEBUG,
    "logging.INFO": logging.INFO,
    "logging.WARNING": logging.WARNING,
    "logging.ERROR": logging.ERROR,
}

logging_level = log_level_info[config["DEFAULT"]["log_level"]]

logging.basicConfig(
    level=logging_level, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)


def start_up_logs():
    logging.info(
        """
             __  ______  ______       ______ ______  ______  __  __       ______  ______  __   __  ______ __  ______    
        /\ \/\  ___\/\  ___\     /\  == /\  __ \/\  ___\/\ \/ /      /\  ___\/\  __ \/\ "-.\ \/\  ___/\ \/\  ___\   
        \ \ \ \ \___\ \  __\     \ \  _-\ \  __ \ \ \___\ \  _"-.    \ \ \___\ \ \/\ \ \ \-.  \ \  __\ \ \ \ \__ \  
         \ \_\ \_____\ \_____\    \ \_\  \ \_\ \_\ \_____\ \_\ \_\    \ \_____\ \_____\ \_\\"\_\ \_\  \ \_\ \_____\ 
          \/_/\/_____/\/_____/     \/_/   \/_/\/_/\/_____/\/_/\/_/     \/_____/\/_____/\/_/ \/_/\/_/   \/_/\/_____/                                                                                                    
        \n
    """
    )


def shut_down_logs():
    logging.info(
        """
        \n
         (              (         )                         )      *      (      (                          
         )\ )     (     )\ )   ( /(   (            (     ( /(    (  `     )\ )   )\ )          *   )        
        (()/(     )\   (()/(   )\())  )\ )         )\    )\())   )\))(   (()/(  (()/(   (    ` )  /(   (    
         /(_))  (((_)   /(_)) ((_)\  (()/(       (((_)  ((_)\   ((_)()\   /(_))  /(_))  )\    ( )(_))  )\   
        (_))    )\___  (_))    _((_)  /(_))_     )\___    ((_)  (_()((_) (_))   (_))   ((_)  (_(_())  ((_)  
        |_ _|  ((/ __| |_ _|  | \| | (_)) __|   ((/ __|  / _ \  |  \/  | | _ \  | |    | __| |_   _|  | __| 
         | |    | (__   | |   | .` |   | (_ |    | (__  | (_) | | |\/| | |  _/  | |__  | _|    | |    | _|  
        |___|    \___| |___|  |_|\_|    \___|     \___|  \___/  |_|  |_| |_|    |____| |___|   |_|    |___|                                                                                               
    """
    )
