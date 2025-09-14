from scraper_functions import fetch_data_from_api, insert_data_into_db, convert_date


def main():
    """Main function to orchestrate data fetching and insertion."""
    
    '''Populate Car Live Queue table'''
    try:
        query = """
        INSERT INTO car_live_queue (
            buffer_zone_id, regnum, status, order_id, type_queue, registration_date, changed_date
        ) VALUES (
            %(buffer_zone_id)s, %(regnum)s, %(status)s, %(order_id)s, %(type_queue)s, %(registration_date)s, %(changed_date)s
        )
        ON CONFLICT (regnum, registration_date) DO NOTHING
        """

        buffer_zones = {
        1: "53d94097-2b34-11ec-8467-ac1f6bf889c0",
        2: "a9173a85-3fc0-424c-84f0-defa632481e4",
        3: "b60677d4-8a00-4f93-a781-e129e1692a03",
        4: "ffe81c11-00d6-11e8-a967-b0dd44bde851",
        }

        for buffer_zone_id, checkpointID in buffer_zones.items():
            url = f"https://belarusborder.by/info/monitoring-new?token=test&checkpointId={checkpointID}"
            data = fetch_data_from_api(url)

            # Iterate over the 'carLiveQueue' and filter by status
            cars_with_status_3 = [car for car in data.get("carLiveQueue", []) if car.get("status") == 3]


            for car in cars_with_status_3:
                car["registration_date"] = convert_date(car["registration_date"])
                car["changed_date"] = convert_date(car["changed_date"])
                insert_data_into_db(buffer_zone_id, query, car)
                print(f"Cars for buffer_zone_id {buffer_zone_id} handled somehow:).")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
