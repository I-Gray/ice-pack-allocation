# Ice Pack Allocator 🧊
Allocates a specified number of ice-packs to a customers box calculated by considering:
- A range of defined temperature bands for different sized cool pouches
- The predicted temperature for the postcode on the planned delivery date of the box
- A set of configurable fall back constants for ranges not explicitly specificed in the range data


## Set-up
1. Clone the repository
2. In the `src` directory, create a file named `config.json` and copy `config.example.json` to the file.
3. Add a valid `meteostat_api_key` in the value section of the secret.
4. In the root director, run the following make command to perform project set-up and run the script:
```commandline
make run-script
```
4. If the run is successful, the output 

## Running Tests
To run the all the unit tests, run the following make command in the root directory:
```commandline
make run-tests
```
Note: ensure the `local-setup` and/or `run-script` have been run first to ensure the requirements are installed.

## Dependencies
This project depends on two external services & the two input files as explained in the next section:
1. [Postcodes.io](https://postcodes.io/docs) - to get the approximate latitude and longitude for a selected **UK** postcode
2. [Meteo Stat API](https://dev.meteostat.net/api/) - to obtain average daily weather data for a given lattitude and longitude

## Input
The Ice Pack Allocator requires the following 2 input files - included in the repo:

```bash
/src/data/Boxes.csv
and 
/src/data/Temperature_bands.csv
```

Below is an outline of the csv columns
```text
Boxes.csv - 
    box_id: str
    delivery_date: datetime
    postcode: str
    Box Size: str
    Cool Pouch Size: str


Temperature_bands.csv - 
    temperature_min: int
    temperature_max: int
    S: int
    M: int
    L: int
```
S, M & L in the `Temperature Bands` refers to the amount of ices that should be assigned for the Small, 
Medium and Large box sizes for that particular range.

## Output
Once the allocator has run, the output is placed here:

```commandline
src/output/orders_assigned_w_ice.csv
```

The schema of this output is: 

```text
orders_assigned_with_ice.csv - 
    box_id: str
    cool_pouch_size: str
    number_of_ices: int
```

## Example Execution Output
```commandline
2023-03-31 17:02:40,961 | root | INFO | 
             __  ______  ______       ______ ______  ______  __  __       ______  ______  __   __  ______ __  ______    
        /\ \/\  ___\/\  ___\     /\  == /\  __ \/\  ___\/\ \/ /      /\  ___\/\  __ \/\ "-.\ \/\  ___/\ \/\  ___\   
        \ \ \ \ \___\ \  __\     \ \  _-\ \  __ \ \ \___\ \  _"-.    \ \ \___\ \ \/\ \ \ \-.  \ \  __\ \ \ \ \__ \  
         \ \_\ \_____\ \_____\    \ \_\  \ \_\ \_\ \_____\ \_\ \_\    \ \_____\ \_____\ \_\"\_\ \_\  \ \_\ \_____\ 
          \/_/\/_____/\/_____/     \/_/   \/_/\/_/\/_____/\/_/\/_/     \/_____/\/_____/\/_/ \/_/\/_/   \/_/\/_____/                                                                                                    
        

    
2023-03-31 17:02:40,961 | root | INFO | Importing data
2023-03-31 17:02:40,961 | root | INFO | reading csv file from - data/Boxes.csv
2023-03-31 17:02:40,968 | root | INFO | csv read successfully
2023-03-31 17:02:40,968 | root | INFO | reading csv file from - data/Temperature_bands.csv
2023-03-31 17:02:40,969 | root | INFO | csv read successfully
2023-03-31 17:02:40,969 | root | INFO | configuring ices...
2023-03-31 17:02:41,960 | root | INFO | ices configured!
2023-03-31 17:02:41,960 | root | INFO | writing csv file to - output/orders_assigned_w_ice.csv
2023-03-31 17:02:41,965 | root | INFO | csv written successfully
2023-03-31 17:02:41,972 | root | INFO | 
        

        output file head - located at output/orders_assigned_w_ice.csv :
        
           box_id cool_pouch_size  number_of_ices
0   GB231               M               2
1  GB1481               M               2
2  GB1681               M               2
    
2023-03-31 17:02:41,972 | root | INFO | 
        

         (              (         )                         )      *      (      (                          
         )\ )     (     )\ )   ( /(   (            (     ( /(    (  `     )\ )   )\ )          *   )        
        (()/(     )\   (()/(   )\())  )\ )         )\    )\())   )\))(   (()/(  (()/(   (    ` )  /(   (    
         /(_))  (((_)   /(_)) ((_)\  (()/(       (((_)  ((_)\   ((_)()\   /(_))  /(_))  )\    ( )(_))  )\   
        (_))    )\___  (_))    _((_)  /(_))_     )\___    ((_)  (_()((_) (_))   (_))   ((_)  (_(_())  ((_)  
        |_ _|  ((/ __| |_ _|  | \| | (_)) __|   ((/ __|  / _ \  |  \/  | | _ \  | |    | __| |_   _|  | __| 
         | |    | (__   | |   | .` |   | (_ |    | (__  | (_) | | |\/| | |  _/  | |__  | _|    | |    | _|  
        |___|    \___| |___|  |_|\_|    \___|     \___|  \___/  |_|  |_| |_|    |____| |___|   |_|    |___| 
```

:)
