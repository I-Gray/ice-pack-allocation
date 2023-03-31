# Ice Pack Allocator 🧊
Allocates a specified number of ice-packs to a customers box calculated by considering:
- A range of defined temperature bands for different sized cool pouches
- The predicted temperature for the postcode on the planned delivery date of the box
- A set of configurable fall back constants for ranges not explicitly specificed in the range data


## Set-up

### Local Execution
1. Clone the repository
2. In the `src` directory, create a file named `config.json` and copy `config.example.json` to the file.
3. Add a valid `meteostat_api_key` in the value section of the secret.
4. In the root director, run the following make command to perform project set-up and run the script:
```commandline
make run-script
```
5. If the run is successful, the output files will be accessible in the `src/output` folder.

### Docker
Before proceeding, ensure youy have docker installed and have the daemon running. If not you can download docker [here](https://docs.docker.com/engine/install/)
1. Run the following command in the root directory of the repo:
```commandline
docker build -t ice-pack-allocator .
```
2. Once the image is built, run:
```commandline
docker run -p 5002:8080 ice-pack-allocator
```
3. If the run is successful, the output files will be accessible in the src/output folder within the container.

## Tests
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
Once the allocator has run, the output/s is placed here:

```commandline
src/output/orders_assigned_w_ice.csv
```
If there are missing postcodes, then the box is skipped and added to a seperate output CSV.
Note: The schema for these missing orders is the `Box` schema that is defined in the `models.py`.
```commandline
src/output/orders_skipped.csv
```

The schema of this output is: 

```text
orders_assigned_with_ice.csv - 
    box_id: str
    cool_pouch_size: str
    number_of_ices: int
```

### Models Schemas
The schemas in the models are slightly altered from the CSV columns to improve readability.
```
@dataclass
class IceTemperatureRanges:
    temp_min: int
    temp_max: int
    small: int
    medium: int
    large: int


@dataclass
class Box:
    box_id: str
    delivery_date: datetime
    postcode: str
    box_size: str
    cool_pouch_size: str


@dataclass
class BoxAssignedIce:
    box_id: str
    cool_pouch_size: str
    number_of_ices: int
```

## Example Output Execution
```commandline
2023-03-31 22:21:32,731 | root | INFO | 
             __  ______  ______       ______ ______  ______  __  __       ______  ______  __   __  ______ __  ______    
        /\ \/\  ___\/\  ___\     /\  == /\  __ \/\  ___\/\ \/ /      /\  ___\/\  __ \/\ "-.\ \/\  ___/\ \/\  ___\   
        \ \ \ \ \___\ \  __\     \ \  _-\ \  __ \ \ \___\ \  _"-.    \ \ \___\ \ \/\ \ \ \-.  \ \  __\ \ \ \ \__ \  
         \ \_\ \_____\ \_____\    \ \_\  \ \_\ \_\ \_____\ \_\ \_\    \ \_____\ \_____\ \_\"\_\ \_\  \ \_\ \_____\ 
          \/_/\/_____/\/_____/     \/_/   \/_/\/_/\/_____/\/_/\/_/     \/_____/\/_____/\/_/ \/_/\/_/   \/_/\/_____/                                                                                                    
        

    
2023-03-31 22:21:32,731 | root | INFO | Importing data
2023-03-31 22:21:32,731 | root | INFO | reading csv file from - data/Boxes.csv
2023-03-31 22:21:32,738 | root | INFO | csv read successfully
2023-03-31 22:21:32,738 | root | INFO | reading csv file from - data/Temperature_bands.csv
2023-03-31 22:21:32,739 | root | INFO | csv read successfully
2023-03-31 22:21:32,739 | root | INFO | configuring ices...
2023-03-31 22:21:33,154 | root | ERROR | err: not found - {"status":404,"error":"Invalid postcode"}
2023-03-31 22:21:33,154 | root | ERROR | err: exception occurred when attempting to get and return latitude and longitude for postcode - 123
2023-03-31 22:21:33,154 | root | INFO | 123 could not be fetched. Skipping box with box_id = GB231
2023-03-31 22:21:40,280 | root | INFO | the following boxes were skipped:
2023-03-31 22:21:40,280 | root | INFO | box_id = GB231, delivery_date = 2022-02-19 00:00:00
2023-03-31 22:21:40,280 | root | INFO | ices configured!
2023-03-31 22:21:40,280 | root | INFO | writing csv file to - output/orders_assigned_w_ice.csv
2023-03-31 22:21:40,286 | root | INFO | csv written successfully
2023-03-31 22:21:40,292 | root | INFO | 
    
        completed boxes head (5 records) - located at output/orders_assigned_w_ice.csv :
           box_id cool_pouch_size  number_of_ices
0   GB231               M               2
1  GB1849               S               2
2   GB880               M               2
3   GB138               M               2
4    GB93               L               2
        
        open the csv file to see the other orders
    
2023-03-31 22:21:40,292 | root | INFO | writing csv file to - output/orders_skipped.csv
2023-03-31 22:21:40,294 | root | INFO | csv written successfully
2023-03-31 22:21:40,300 | root | INFO | 
    
        missing boxes head (5 records) - located at output/orders_skipped.csv :
          box_id delivery_date  postcode box_size cool_pouch_size
0  GB231    2022-02-19       123        L               M
        
        open the csv file to see the other orders (if any)
    
2023-03-31 22:21:40,300 | root | INFO | 
        

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
