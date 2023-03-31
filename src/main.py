import logging
import time

from config import start_up_logs, shut_down_logs, config
from domain.data_handle import import_data
from domain.weather_service import WeatherService
from domain.icepack_configurator import IcePackConfigurator
from utils import write_csv, log_output_file_head


def main():
    # Start-up sequence
    start_up_logs()

    # Get data from csv files
    data_filepath = "data/"
    boxes, temperature_ranges = import_data(data_filepath)

    # Initialise weather service
    ws = WeatherService(api_key=config["SECRET"]["meteostat_api_key"])

    # Ice-pack configurator logic
    icepack_config = IcePackConfigurator(
        boxes=boxes,
        temperature_ranges=temperature_ranges,
        get_temp=ws.get_daily_temperature_avg,
    )
    boxes_with_ice, skipped_boxes = icepack_config.pack_boxes_with_ices()

    # Write output to assigned boxes CSV file
    output_filepath = "output/orders_assigned_w_ice.csv"
    write_csv(output_filepath, boxes_with_ice)
    log_output_file_head(output_filepath, "completed")

    # Write output for missing boxes to CSV
    output_filepath = "output/orders_skipped.csv"
    write_csv(output_filepath, skipped_boxes)
    log_output_file_head(output_filepath, "missing")

    # Shutdown sequence
    shut_down_logs()
    time.sleep(120)
    logging.info('script complete')


if __name__ == "__main__":
    main()
